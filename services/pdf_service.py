"""
LaundryBot V7 Enterprise
PDF Service
"""

import hashlib
import fitz  # PyMuPDF

from database.db import connect


class PDFService:

    # ==========================================
    # Import PDF -> documents
    # ==========================================

    def import_pdf(
        self,
        filepath,
        filename,
        document_type,
        model="",
        category="",
    ):

        doc = fitz.open(filepath)

        conn = connect()

        imported = 0

        file_hash = self.sha256(filepath)

        # ลบข้อมูลเดิมก่อน (Import ใหม่)
        conn.execute(
            """
            DELETE FROM documents
            WHERE filename=?
            """,
            (filename,),
        )

        # เพิ่มทีละหน้า
        for page_no in range(len(doc)):

            page = doc.load_page(page_no)

            text = page.get_text("text")

            if text.strip() == "":
                continue

            conn.execute(
                """
                INSERT INTO documents(

                    filename,
                    document_type,
                    model,
                    category,
                    page,
                    content,
                    file_hash

                )

                VALUES(
                    ?,?,?,?,?,?,?
                )
                """,
                (
                    filename,
                    document_type,
                    model,
                    category,
                    page_no + 1,
                    text,
                    file_hash,
                ),
            )

            imported += 1

        conn.commit()

        doc.close()

        return imported

    # ==========================================
    # SHA256
    # ==========================================

    def sha256(self, filepath):

        sha = hashlib.sha256()

        with open(filepath, "rb") as f:

            while True:

                block = f.read(65536)

                if not block:
                    break

                sha.update(block)

        return sha.hexdigest()

    # ==========================================
    # Read PDF
    # ==========================================

    def read(self, filepath):

        doc = fitz.open(filepath)

        text = ""

        for page in doc:

            text += page.get_text("text")

        doc.close()

        return text

    # ==========================================
    # Get Pages
    # ==========================================

    def get_pages(self, filename):

        conn = connect()

        return conn.execute(
            """
            SELECT *

            FROM documents

            WHERE filename=?

            ORDER BY page
            """,
            (filename,),
        ).fetchall()

    # ==========================================
    # Search
    # ==========================================

    def search(self, keyword):

        conn = connect()

        return conn.execute(
            """
            SELECT *

            FROM documents

            WHERE content LIKE ?

            LIMIT 100
            """,
            (f"%{keyword}%",),
        ).fetchall()
    # =====================================================
    # Import Upload File
    # =====================================================

    def import_upload(

        self,

        file,

        upload_folder,

        document_type,

        model="",

        category="",

    ):

        import os

        os.makedirs(
            upload_folder,
            exist_ok=True,
        )

        filepath = os.path.join(

            upload_folder,

            file.filename,

        )

        file.save(filepath)

        pages = self.import_pdf(

            filepath=filepath,

            filename=file.filename,

            document_type=document_type,

            model=model,

            category=category,

        )

        return pages


pdf_service = PDFService()