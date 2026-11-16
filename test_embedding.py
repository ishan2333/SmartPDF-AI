import ollama

response = ollama.embed(
    model="nomic-embed-text",
    input="Python is a programming language."
)

print(response["embeddings"])