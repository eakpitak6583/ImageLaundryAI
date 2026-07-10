"""
LaundryBot V5

PDF Reader
"""

from pathlib import Path
from pypdf import PdfReader


def read_pdf(pdf_file):

    pdf_file = Path(pdf_file)

    reader = PdfReader(str(pdf_file))

    text = []

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:

            text.append(page_text)

    return "\n".join(text)