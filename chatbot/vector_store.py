import os
import json
import ollama
import faiss
import numpy as np

from pathlib import Path
from django.conf import settings
from .models import DocumentChunk


MODEL_NAME = "nomic-embed-text"


def create_vector_store(document_id):

    # Get all chunks for this PDF
    chunks = DocumentChunk.objects.filter(
        document_id=document_id
    ).order_by("chunk_index")

    if not chunks.exists():
        raise ValueError("No chunks found for this document.")

    texts = [chunk.content for chunk in chunks]

    # Generate embeddings
    response = ollama.embed(
        model=MODEL_NAME,
        input=texts
    )

    embeddings = np.array(
        response["embeddings"],
        dtype=np.float32
    )

    # Normalize vectors for cosine similarity
    faiss.normalize_L2(embeddings)

    # Create FAISS index
    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)

    # Create storage directory
    save_path = (
        Path(settings.MEDIA_ROOT)
        / "vectorstores"
        / f"document_{document_id}"
    )

    os.makedirs(save_path, exist_ok=True)

    # Save FAISS index
    faiss.write_index(
        index,
        str(save_path / "index.faiss")
    )

    # Save chunk information
    metadata = []

    for chunk in chunks:
        metadata.append({
            "chunk_id": chunk.id,
            "page_number": chunk.page_number,
            "chunk_index": chunk.chunk_index,
            "content": chunk.content
        })

    with open(save_path / "metadata.json", "w", encoding="utf-8") as file:
        json.dump(metadata, file, ensure_ascii=False, indent=4)

    return len(chunks)

def search_chunks(document_id, query, top_k=3):

    # Locate vector database
    save_path = (
        Path(settings.MEDIA_ROOT)
        / "vectorstores"
        / f"document_{document_id}"
    )

    index_path = save_path / "index.faiss"
    metadata_path = save_path / "metadata.json"

    # Load FAISS index
    index = faiss.read_index(str(index_path))

    # Load metadata
    with open(metadata_path, "r", encoding="utf-8") as file:
        metadata = json.load(file)

    # Generate question embedding
    response = ollama.embed(
        model=MODEL_NAME,
        input=query
    )

    query_embedding = np.array(
        response["embeddings"],
        dtype=np.float32
    )

    # Normalize question vector
    faiss.normalize_L2(query_embedding)

    # Search relevant chunks
    scores, indices = index.search(
        query_embedding,
        min(top_k, index.ntotal)
    )

    results = []

    for score, idx in zip(scores[0], indices[0]):

        if idx == -1:
            continue

        result = metadata[idx].copy()
        result["score"] = float(score)

        results.append(result)

    return results