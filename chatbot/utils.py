import fitz

def extract_text_from_pdf(pdf_path):
    extracted_text = ""

    pdf = fitz.open(pdf_path)

    for page_number, page in enumerate(pdf):
        text = page.get_text()

        extracted_text += (
            f"\n\n--- Page {page_number + 1} ---\n"
            + text
        )

    pdf.close()

    return extracted_text


import re

def split_text_into_chunks(
    extracted_text,
    chunk_size=1000,
    overlap=150
):
    chunks = []

    page_markers = list(
        re.finditer(r"--- Page (\d+) ---", extracted_text)
    )

    for i, marker in enumerate(page_markers):

        page_number = int(marker.group(1))

        start = marker.end()
        end = (
            page_markers[i + 1].start()
            if i + 1 < len(page_markers)
            else len(extracted_text)
        )

        page_text = extracted_text[start:end].strip()

        position = 0

        while position < len(page_text):

            chunk_end = min(
                position + chunk_size,
                len(page_text)
            )

            if chunk_end < len(page_text):
                space_position = page_text.rfind(
                    " ", position, chunk_end
                )

                if space_position > position + chunk_size * 0.7:
                    chunk_end = space_position

            content = page_text[position:chunk_end].strip()

            if content:
                chunks.append({
                    "page_number": page_number,
                    "content": content
                })

            if chunk_end >= len(page_text):
                break

            position = max(
                chunk_end - overlap,
                position + 1
            )

    return chunks