
from pypdf import PdfReader
from io import BytesIO


def extract_text_from_pdf(file):
    """
    Extract text content from an uploaded PDF resume.
    """

    try:
        pdf_reader = PdfReader(BytesIO(file))

        extracted_text = ""

        for page in pdf_reader.pages:
            page_text = page.extract_text()

            if page_text:
                extracted_text += page_text + "\n"

        if not extracted_text.strip():
            raise ValueError("No readable text found in the PDF.")

        return extracted_text.strip()

    except Exception as error:
        raise ValueError(f"Could not process PDF: {error}")
