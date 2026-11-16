
from django import forms
from .models import PDFDocument


class PDFUploadForm(forms.ModelForm):

    class Meta:
        model = PDFDocument
        fields = ["title", "pdf_file"]

    def clean_pdf_file(self):

        pdf_file = self.cleaned_data.get("pdf_file")

        # Check file size (maximum 10 MB)
        if pdf_file.size > 10 * 1024 * 1024:
            raise forms.ValidationError(
                "PDF file size must be less than 10 MB."
            )

        # Check file extension
        if not pdf_file.name.lower().endswith(".pdf"):
            raise forms.ValidationError(
                "Only PDF files are allowed."
            )

        # Check PDF file signature
        header = pdf_file.read(5)
        pdf_file.seek(0)

        if header != b"%PDF-":
            raise forms.ValidationError(
                "Invalid PDF file."
            )

        return pdf_file
