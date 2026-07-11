"""
LaundryBot V7 Enterprise
PDF Service
"""

import hashlib
import logging
from pathlib import Path

import fitz  # PyMuPDF

from database.db import (
    connect,
)

logger = logging.getLogger(
    __name__,
)


class PDFService:

    # ==========================================================
    # Constructor
    # ==========================================================

    def __init__(

        self,

    ):

        logger.info(

            "PDF Service Initialized"

        )

    # ==========================================================
    # SHA256
    # ==========================================================

    def sha256(

        self,

        filepath,

    ):

        sha = hashlib.sha256()

        with open(

            filepath,

            "rb",

        ) as f:

            for chunk in iter(

                lambda: f.read(65536),

                b"",

            ):

                sha.update(

                    chunk,

                )

        return sha.hexdigest()
    # ==========================================================
    # Import PDF
    # ==========================================================

    def import_pdf(

        self,

        filepath,

        filename,

        document_type,

        model="",

        category="",

    ):

        logger.info(

            "Import PDF : %s",

            filename,

        )

        conn = connect()

        doc = None

        imported = 0

        try:

            doc = fitz.open(

                filepath,

            )

            file_hash = self.sha256(

                filepath,

            )

            logger.info(

                "Replacing existing document : %s",

                filename,

            )

            conn.execute(

                """

                DELETE

                FROM documents

                WHERE filename = ?

                """,

                (

                    filename,

                ),

            )

            for page_no in range(

                len(doc),

            ):

                page = doc.load_page(

                    page_no,

                )

                text = page.get_text(

                    "text",

                ).strip()

                if text == "":

                    continue

                conn.execute(

                    """

                    INSERT INTO documents
                    (

                        filename,

                        document_type,

                        model,

                        category,

                        page,

                        content,

                        file_hash

                    )

                    VALUES
                    (
                        ?, ?, ?, ?, ?, ?, ?
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

            logger.info(

                "Imported %s pages.",

                imported,

            )

            return imported

        except Exception as e:

            conn.rollback()

            logger.exception(

                "PDF import failed: %s",

                e,

            )

            raise

        finally:

            if doc is not None:

                doc.close()

            conn.close()
    # ==========================================================
    # Read PDF
    # ==========================================================

    def read(

        self,

        filepath,

    ):

        logger.info(

            "Reading PDF : %s",

            filepath,

        )

        doc = None

        try:

            doc = fitz.open(

                filepath,

            )

            texts = []

            for page in doc:

                text = page.get_text(

                    "text",

                ).strip()

                if text:

                    texts.append(

                        text,

                    )

            logger.info(

                "PDF read completed."

            )

            return "\n".join(

                texts,

            )

        except Exception as e:

            logger.exception(

                "Unable to read PDF: %s",

                e,

            )

            raise

        finally:

            if doc is not None:

                doc.close()

    # ==========================================================
    # Get Pages
    # ==========================================================

    def get_pages(

        self,

        filename,

    ):

        logger.info(

            "Loading document pages : %s",

            filename,

        )

        conn = connect()

        try:

            rows = conn.execute(

                """

                SELECT *

                FROM documents

                WHERE filename = ?

                ORDER BY page

                """,

                (

                    filename,

                ),

            ).fetchall()

            logger.info(

                "Loaded %s pages.",

                len(rows),

            )

            return rows

        except Exception as e:

            logger.exception(

                "Unable to load document pages: %s",

                e,

            )

            raise

        finally:

            conn.close()
    # ==========================================================
    # Search
    # ==========================================================

    def search(

        self,

        keyword,

        limit=100,

    ):

        keyword = str(

            keyword or "",

        ).strip()

        if keyword == "":

            return []

        logger.info(

            "Document Search : %s",

            keyword,

        )

        conn = connect()

        try:

            rows = conn.execute(

                """

                SELECT *

                FROM documents

                WHERE

                    content LIKE ?

                    OR filename LIKE ?

                    OR model LIKE ?

                    OR category LIKE ?

                ORDER BY

                    filename,

                    page

                LIMIT ?

                """,

                (

                    f"%{keyword}%",

                    f"%{keyword}%",

                    f"%{keyword}%",

                    f"%{keyword}%",

                    limit,

                ),

            ).fetchall()

            logger.info(

                "Search returned %s rows.",

                len(rows),

            )

            return rows

        except Exception as e:

            logger.exception(

                "Document search failed: %s",

                e,

            )

            raise

        finally:

            conn.close()

    # ==========================================================
    # Import Upload File
    # ==========================================================

    def import_upload(

        self,

        file,

        upload_folder,

        document_type,

        model="",

        category="",

    ):

        logger.info(

            "Uploading PDF : %s",

            file.filename,

        )

        upload_path = Path(

            upload_folder,

        )

        upload_path.mkdir(

            parents=True,

            exist_ok=True,

        )

        filepath = upload_path / Path(

            file.filename,

        ).name

        file.save(

            filepath,

        )

        logger.info(

            "PDF saved : %s",

            filepath,

        )

        return self.import_pdf(

            filepath=str(

                filepath,

            ),

            filename=filepath.name,

            document_type=document_type,

            model=model,

            category=category,

        )
    # ==========================================================
    # Health
    # ==========================================================

    def health(

        self,

    ):

        logger.info(

            "PDF Service Health Check"

        )

        return {

            "success": True,

            "service": "pdf_service",

            "status": "ok",

        }

    # ==========================================================
    # Version
    # ==========================================================

    def version(

        self,

    ):

        return {

            "name": "LaundryBot V7 Enterprise",

            "module": "PDF Service",

            "version": getattr(

                Config,

                "VERSION",

                "7.0",

            ),

        }

    # ==========================================================
    # File Exists
    # ==========================================================

    def exists(

        self,

        filepath,

    ):

        return Path(

            filepath,

        ).exists()

    # ==========================================================
    # Page Count
    # ==========================================================

    def page_count(

        self,

        filepath,

    ):

        logger.info(

            "Counting PDF pages : %s",

            filepath,

        )

        doc = None

        try:

            doc = fitz.open(

                filepath,

            )

            return len(

                doc,

            )

        except Exception as e:

            logger.exception(

                "Unable to count PDF pages: %s",

                e,

            )

            raise

        finally:

            if doc is not None:

                doc.close()
# ==========================================================
# Rebuild Database
# ==========================================================

    def rebuild(

        self,

    ):

        logger.info(

            "Rebuilding PDF database..."

        )

        return self.build()

    # ==========================================================
    # Statistics
    # ==========================================================

    def total_documents(

        self,

    ):

        conn = connect()

        try:

            row = conn.execute(

                """

                SELECT

                    COUNT(*) AS total

                FROM documents

                """

            ).fetchone()

            if row is None:

                return 0

            return row["total"]

        finally:

            conn.close()

    # ==========================================================
    # Total Files
    # ==========================================================

    def total_files(

        self,

    ):

        conn = connect()

        try:

            row = conn.execute(

                """

                SELECT

                    COUNT(

                        DISTINCT filename

                    ) AS total

                FROM documents

                """

            ).fetchone()

            if row is None:

                return 0

            return row["total"]

        finally:

            conn.close()


# ==========================================================
# Singleton
# ==========================================================

pdf_service = PDFService()