"""
LaundryBot V7 Enterprise
PDF Service
"""

import hashlib
import logging
from pathlib import Path

import fitz  # PyMuPDF

from config import (
    Config,
)

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

        ) as file:

            for chunk in iter(

                lambda: file.read(65536),

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

                "Removing previous document : %s",

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

            for page_number in range(

                len(doc),

            ):

                page = doc.load_page(

                    page_number,

                )

                text = page.get_text(

                    "text",

                ).strip()

                if not text:

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

                        page_number + 1,

                        text,

                        file_hash,

                    ),

                )

                imported += 1

            conn.commit()

            logger.info(

                "Imported %s pages from %s",

                imported,

                filename,

            )

            return imported

        except Exception as e:

            conn.rollback()

            logger.exception(

                "Import PDF failed: %s",

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

            pages = []

            for page in doc:

                text = page.get_text(

                    "text",

                ).strip()

                if text:

                    pages.append(

                        text,

                    )

            logger.info(

                "PDF read successfully."

            )

            return "\n".join(

                pages,

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

            "Loading pages : %s",

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

                "Unable to load pages: %s",

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

        if not keyword:

            logger.warning(

                "Empty search keyword."

            )

            return []

        logger.info(

            "Searching documents : %s",

            keyword,

        )

        conn = connect()

        try:

            rows = conn.execute(

                """

                SELECT *

                FROM documents

                WHERE

                    filename LIKE ?

                    OR document_type LIKE ?

                    OR model LIKE ?

                    OR category LIKE ?

                    OR content LIKE ?

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

                    f"%{keyword}%",

                    limit,

                ),

            ).fetchall()

            logger.info(

                "Found %s document(s).",

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
    # Import Upload
    # ==========================================================

    def import_upload(

        self,

        file,

        upload_folder,

        document_type,

        model="",

        category="",

    ):

        if file is None:

            raise ValueError(

                "File is required."

            )

        if not file.filename:

            raise ValueError(

                "Filename is required."

            )

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

        filename = Path(

            file.filename,

        ).name

        filepath = upload_path / filename

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

            filename=filename,

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

        conn = connect()

        try:

            conn.execute(

                "SELECT 1"

            ).fetchone()

            database = True

        except Exception:

            database = False

        finally:

            conn.close()

        return {

            "success": True,

            "service": "pdf_service",

            "database": database,

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

        ).is_file()

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
    # Total Documents
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

            return row["total"] if row else 0

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

            return row["total"] if row else 0

        finally:

            conn.close()
# ==========================================================
# End of Class
# ==========================================================


# ==========================================================
# Singleton
# ==========================================================

pdf_service = PDFService()
