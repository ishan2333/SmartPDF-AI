
# SmartPDF-RAG

An AI-powered PDF Question Answering System built using Django and Retrieval-Augmented Generation (RAG).

Upload PDF documents and ask questions about their content. The system retrieves relevant information using semantic search and generates answers using a locally running LLM.

## Features

- Upload and process PDF documents
- Extract text using PyMuPDF
- Split documents into smaller text chunks
- Generate embeddings using Ollama
- Store and search embeddings using FAISS
- Generate contextual answers using Llama 3.2
- Display relevant source pages
- Integrated PDF viewer
- Persistent chat history for each document
- Automatic FAISS vector-store creation
- Automatic recovery of missing vector indexes
- PDF upload validation and error handling

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Django | Web framework |
| PyMuPDF | PDF text extraction |
| Ollama | Local AI model execution |
| Nomic Embed Text | Text embeddings |
| Llama 3.2 | Answer generation |
| FAISS | Vector similarity search |
| NumPy | Numerical operations |
| HTML, CSS, JavaScript | Frontend |
| SQLite | Database |

## Project Structure

```text
SmartPDF-Django/
│
├── chatbot/
│   ├── migrations/
│   ├── templates/
│   │   └── chatbot/
│   │       └── home.html
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── utils.py
│   ├── vector_store.py
│   ├── rag.py
│   └── urls.py
│
├── config/
│   ├── settings.py
│   └── urls.py
│
├── media/
├── manage.py
├── requirements.txt
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd SmartPDF-Django
```

### 2. Create a virtual environment

```bash
python -m venv env
```

### 3. Activate the environment

Windows:

```powershell
.\env\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Install and configure Ollama

Install Ollama and pull the required models:

```bash
ollama pull nomic-embed-text
ollama pull llama3.2
```

Make sure Ollama is running.

### 6. Apply database migrations

```bash
python manage.py migrate
```

### 7. Start the Django server

```bash
python manage.py runserver
```

Open:

http://127.0.0.1:8000/

## How It Works

1. User uploads a PDF document.
2. PyMuPDF extracts text from the PDF.
3. Extracted text is divided into smaller chunks.
4. Ollama generates embeddings for the chunks.
5. FAISS stores the vectors for semantic search.
6. User submits a question.
7. FAISS retrieves relevant document chunks.
8. Llama 3.2 generates an answer using the retrieved context.
9. The answer and source information are returned to the user.

## AI Models

- Embedding Model: nomic-embed-text
- Language Model: llama3.2

## Future Improvements

- OCR support for scanned PDFs
- User authentication
- Cloud deployment
- Support for multiple document formats

## Author

Developed as a Computer Engineering project by -ISHAN AJINATH KHEDKAR.
