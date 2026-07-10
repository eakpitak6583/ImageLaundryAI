import fitz


def read_pdf(pdf_path):

    doc = fitz.open(pdf_path)

    pages = []

    for page in doc:

        pages.append(page.get_text())

    doc.close()

    return pages