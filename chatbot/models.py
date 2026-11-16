from django.db import models

class PDFDocument(models.Model):
    title = models.CharField(max_length=255)
    pdf_file = models.FileField(upload_to="pdfs/")
    extracted_text = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class DocumentChunk(models.Model):
    document = models.ForeignKey(
        PDFDocument,
        on_delete=models.CASCADE,
        related_name="chunks"
    )

    page_number = models.IntegerField()
    chunk_index = models.IntegerField()
    content = models.TextField()

    def __str__(self):
        return f"{self.document.title} - Chunk {self.chunk_index}"        

class ChatMessage(models.Model):
    document = models.ForeignKey(
        PDFDocument,
        on_delete=models.CASCADE,
        related_name="chat_messages"
    )
    question = models.TextField()
    answer = models.TextField()
    sources = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.question[:50]        