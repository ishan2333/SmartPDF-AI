from django.shortcuts import render, redirect
from .forms import PDFUploadForm
from .models import PDFDocument, DocumentChunk
from .utils import (
    extract_text_from_pdf,
    split_text_into_chunks
)

from django.http import JsonResponse
from .rag import ask_pdf
from .models import PDFDocument, DocumentChunk, ChatMessage
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .vector_store import create_vector_store
import os
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def home(request):

    # Initialize form for GET requests
    form = PDFUploadForm()

    if request.method == "POST":

        form = PDFUploadForm(request.POST, request.FILES)

        if form.is_valid():

            document = form.save()

            try:
                # Extract PDF text
                extracted_text = extract_text_from_pdf(
                    document.pdf_file.path
                )

                if not extracted_text.strip():
                    raise ValueError(
                        "This PDF contains no extractable text."
                    )

                document.extracted_text = extracted_text
                document.save()

                # Split text into chunks
                chunks = split_text_into_chunks(extracted_text)

                if not chunks:
                    raise ValueError(
                        "No text chunks could be generated."
                    )

                # Save chunks
                chunk_objects = []

                for index, chunk in enumerate(chunks):
                    chunk_objects.append(
                        DocumentChunk(
                            document=document,
                            page_number=chunk["page_number"],
                            chunk_index=index + 1,
                            content=chunk["content"]
                        )
                    )

                DocumentChunk.objects.bulk_create(chunk_objects)

                # Create FAISS vector store
                create_vector_store(document.id)

                return redirect("home")

            except Exception:
                # Log the actual error in the terminal
                logger.exception("PDF processing failed")

                # Delete failed document
                document.pdf_file.delete(save=False)
                document.delete()

                form.add_error(
                    "pdf_file",
                    "Unable to process this PDF. Please upload a valid, text-based PDF."
                )

    documents = PDFDocument.objects.order_by("-uploaded_at")

    return render(
        request,
        "chatbot/home.html",
        {
            "form": form,
            "documents": documents
        }
    )




def chat(request):
    if request.method == "POST":
        try:
            document_id = request.POST.get("document_id")
            question = request.POST.get("question")

            if not document_id or not question:
                return JsonResponse({
                    "error": "Document and question are required."
                }, status=400)

            document = get_object_or_404(
                PDFDocument,
                id=document_id
            )

            # Check whether FAISS files exist
            vector_dir = os.path.join(
                settings.MEDIA_ROOT,
                "vectorstores",
                f"document_{document.id}"
            )

            index_path = os.path.join(vector_dir, "index.faiss")
            metadata_path = os.path.join(vector_dir, "metadata.json")

            if not os.path.exists(index_path) or not os.path.exists(metadata_path):

                # Check whether document chunks exist
                if not DocumentChunk.objects.filter(document=document).exists():
                    return JsonResponse({
                        "error": "No document chunks found. Please upload the PDF again."
                    }, status=400)

                # Rebuild missing vector store
                create_vector_store(document.id)

            # Generate AI answer
            result = ask_pdf(document.id, question)

            # Save conversation in database
            ChatMessage.objects.create(
                document=document,
                question=question,
                answer=result["answer"],
                sources=result["sources"]
            )

            return JsonResponse(result)

        except Exception:
            logger.exception("Error while processing chat request")

            return JsonResponse({
                "error": "Something went wrong while generating your answer. Please try again."
            }, status=500)

            return JsonResponse({
                "error": "Invalid request method."
            }, status=405)

def chat_history(request, document_id):

    messages = ChatMessage.objects.filter(
        document_id=document_id
    ).order_by("created_at")

    data = []

    for message in messages:

        data.append({
            "question": message.question,
            "answer": message.answer,
            "sources": message.sources,
            "created_at": message.created_at.strftime(
                "%d %b %Y, %I:%M %p"
            )
        })

    return JsonResponse({
        "messages": data
    })   