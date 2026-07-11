"""
LaundryBot V7 Enterprise
Document Service
"""

import hashlib
import logging
from pathlib import Path

from flask import (
    send_file,
)

from config import (
    Config,
)

from database.db import (
    connect,
)

from repositories.document_repository import (
    document_repository,
)

from services.base_service import (
    BaseService,
)

from services.embedding_service import (
    embedding_service,
)

from services.pdf_service import (
    pdf_service,
)


logger = logging.getLogger(
    __name__,
)


class DocumentService(BaseService):

    # ==========================================================
    # Constructor
    # ==========================================================

    def __init__(

        self,

    ):

        super().__init__()

        self.repo = document_repository

        self.upload_path = Path(

            Config.UPLOAD_FOLDER,

        )

        logger.info(

            "Document Service Initialized"

        )

    # ==========================================================
    # Read
    # ==========================================================

    def get_all(

        self,

    ):

        return self.repo.get_all()

    def get(

        self,

        document_id,

    ):

        return self.repo.get(

            document_id,

        )

    def search(

        self,

        keyword,

    ):

        return self.repo.search(

            keyword,

        )

    # ==========================================================
    # Import Logs
    # ==========================================================

    def import_logs(

        self,

    ):

        logger.info(

            "Loading import logs..."

        )

        conn = connect()

        try:

            rows = conn.execute(

                """
                SELECT *

                FROM import_logs

                ORDER BY

                    imported_at DESC,

                    id DESC
                """

            ).fetchall()

            return rows

        finally:

            conn.close()
    # ==========================================================
    # Create
    # ==========================================================

    def create(

        self,

        data,

    ):

        logger.info(

            "Creating document..."

        )

        filename = str(

            data.get(

                "filename",

                "",

            )

        ).strip()

        if filename == "":

            return self.error(

                "Filename is required"

            )

        content = str(

            data.get(

                "content",

                "",

            )

        )

        if not data.get(

            "file_hash",

        ):

            source = (

                filename

                + content

            )

            data["file_hash"] = hashlib.sha256(

                source.encode(

                    "utf-8",

                )

            ).hexdigest()

        document_id = self.repo.create(

            data,

        )

        logger.info(

            "Document created : %s",

            document_id,

        )

        return {

            "success": True,

            "document_id": document_id,

            "data": document_id,

        }

    # ==========================================================
    # Import PDF
    # ==========================================================

    def import_pdf(

        self,

        files,

        form,

    ):

        logger.info(

            "Import PDF Started"

        )

        file = files.get(

            "file",

        )

        if file is None:

            return self.error(

                "PDF file is required"

            )

        if file.filename == "":

            return self.error(

                "Filename is required"

            )

        category = form.get(

            "category",

            "manual",

        )

        model = form.get(

            "machine_model",

            "",

        )

        self.upload_path.mkdir(

            parents=True,

            exist_ok=True,

        )

        filename = Path(

            file.filename,

        ).name

        filepath = self.upload_path / filename

        file.save(

            filepath,

        )

        logger.info(

            "PDF Saved : %s",

            filepath,

        )

        pages = pdf_service.import_pdf(

            filepath=str(

                filepath,

            ),

            filename=filename,

            document_type=category,

            model=model,

            category=category,

        )

        logger.info(

            "Imported %s pages.",

            pages,

        )

        return {

            "success": True,

            "pages": pages,

            "filename": filename,

        }
    # ==========================================================
    # Update
    # ==========================================================

    def update(

        self,

        document_id,

        data,

    ):

        logger.info(

            "Updating document : %s",

            document_id,

        )

        document = self.repo.get(

            document_id,

        )

        if document is None:

            return self.error(

                "Document not found"

            )

        filename = str(

            data.get(

                "filename",

                document.get(

                    "filename",

                    "",

                ),

            )

        ).strip()

        content = str(

            data.get(

                "content",

                document.get(

                    "content",

                    "",

                ),

            )

        )

        source = (

            filename

            + content

        )

        data["file_hash"] = hashlib.sha256(

            source.encode(

                "utf-8",

            )

        ).hexdigest()

        self.repo.update(

            document_id,

            data,

        )

        logger.info(

            "Document updated : %s",

            document_id,

        )

        return self.success()

    # ==========================================================
    # Delete
    # ==========================================================

    def delete(

        self,

        document_id,

    ):

        logger.info(

            "Deleting document : %s",

            document_id,

        )

        document = self.repo.get(

            document_id,

        )

        if document is None:

            return self.error(

                "Document not found"

            )

        self.repo.delete(

            document_id,

        )

        logger.info(

            "Document deleted : %s",

            document_id,

        )

        return self.success()
    # ==========================================================
    # Latest
    # ==========================================================

    def latest(

        self,

        limit=20,

    ):

        logger.info(

            "Loading latest documents..."

        )

        if hasattr(

            self.repo,

            "latest",

        ):

            return self.repo.latest(

                limit,

            )

        documents = self.repo.get_all()

        return documents[:limit]

    # ==========================================================
    # Statistics
    # ==========================================================

    def total(

        self,

    ):

        logger.info(

            "Counting documents..."

        )

        if hasattr(

            self.repo,

            "total",

        ):

            return self.repo.total()

        return len(

            self.repo.get_all()

        )

    # ==========================================================
    # Rebuild Embedding
    # ==========================================================

    def rebuild_embedding(

        self,

    ):

        logger.info(

            "Rebuilding embedding database..."

        )

        try:

            pages = embedding_service.build()

            logger.info(

                "Embedding rebuilt : %s pages",

                pages,

            )

            return {

                "success": True,

                "pages": pages,

            }

        except Exception as e:

            logger.exception(

                e,

            )

            return self.error(

                "Vector rebuild failed."

            )
    # ==========================================================
    # View PDF
    # ==========================================================

    def view_pdf(

        self,

        filename,

    ):

        logger.info(

            "Opening PDF : %s",

            filename,

        )

        filename = Path(

            filename,

        ).name

        pdf = self.upload_path / filename

        if not pdf.exists():

            logger.warning(

                "PDF not found : %s",

                pdf,

            )

            raise FileNotFoundError(

                filename,

            )

        return send_file(

            pdf,

            mimetype="application/pdf",

            as_attachment=False,

            download_name=filename,

        )

    # ==========================================================
    # Download PDF
    # ==========================================================

    def download_pdf(

        self,

        filename,

    ):

        logger.info(

            "Downloading PDF : %s",

            filename,

        )

        filename = Path(

            filename,

        ).name

        pdf = self.upload_path / filename

        if not pdf.exists():

            logger.warning(

                "PDF not found : %s",

                pdf,

            )

            raise FileNotFoundError(

                filename,

            )

        return send_file(

            pdf,

            mimetype="application/pdf",

            as_attachment=True,

            download_name=filename,

        )
    # ==========================================================
    # Health
    # ==========================================================

    def health(

        self,

    ):

        logger.info(

            "Document Service Health Check"

        )

        return {

            "success": True,

            "service": "document_service",

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

            "module": "Document Service",

            "version": "7.0",

        }


# ==========================================================
# Singleton
# ==========================================================

document_service = DocumentService()
