"""
LaundryBot V6

Parser Engine
"""

from importer.engine.document import Document
from importer.engine.line import Line


def build_document(text):

    doc = Document(text)

    for row in text.splitlines():

        row = row.strip()

        if not row:

            continue

        doc.add(

            Line(row)

        )

    return doc