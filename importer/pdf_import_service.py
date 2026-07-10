"""
LaundryBot V5

Import PDF Folder
"""

from pathlib import Path
from pypdf import PdfReader


# ==========================================================
# Read PDF
# ==========================================================

def read_pdf(pdf_path):

    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:

            text += page_text + "\n"

    return text


# ==========================================================
# Import Folder
# ==========================================================

def import_folder(folder):

    folder = Path(folder)

    pdf_files = sorted(folder.glob("*.pdf"))

    print("=" * 70)
    print("LaundryBot PDF Import")
    print("=" * 70)

    print(f"พบ {len(pdf_files)} PDF\n")

    for pdf in pdf_files:

        print("-" * 60)

        print(pdf.name)

        try:

            text = read_pdf(pdf)

            print(text[:800])

        except Exception as e:

            print(e)