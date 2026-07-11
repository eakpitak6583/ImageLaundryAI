"""
LaundryBot V7 Enterprise
Document Service
"""

import hashlib
import logging
from pathlib import (
    Path,
)

from flask import (
    send_file,
)

from config import (
    Config,
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

from services.rag_service import (
    rag_service,
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

        ).resolve()

        self.upload_path.mkdir(

            parents=True,

            exist_ok=True,

        )

        logger.info(

            "Document Service Initialized",

        )

    # ==========================================================
    # Build Hash
    # ==========================================================

    def build_hash(

        self,

        filename,

        content,

    ):

        source = (

            str(

                filename or "",

            )

            +

            str(

                content or "",

            )

        )

        return hashlib.sha256(

            source.encode(

                "utf-8",

            )

        ).hexdigest()

    # ==========================================================
    # Validate Filename
    # ==========================================================

    def validate_filename(

        self,

        filename,

    ):

        filename = str(

            filename or "",

        ).strip()

        if filename == "":

            raise ValueError(

                "Filename is required.",

            )

        return Path(

            filename,

        ).name

    # ==========================================================
    # Validate Upload
    # ==========================================================

    def validate_upload(

        self,

        file,

    ):

        if file is None:

            raise ValueError(

                "PDF file is required.",

            )

        filename = self.validate_filename(

            getattr(

                file,

                "filename",

                "",

            )

        )

        if not filename.lower().endswith(

            ".pdf",

        ):

            raise ValueError(

                "Only PDF files are supported.",

            )

        return filename

    # ==========================================================
    # Rebuild Vector Database
    # ==========================================================

    def rebuild_vector(

        self,

    ):

        logger.info(

            "Rebuilding vector database...",

        )

        pages = embedding_service.rebuild()

        rag_service.reload()

        logger.info(

            "Vector database rebuilt successfully.",

        )

        return pages

    # ==========================================================
    # Read
    # ==========================================================

    def get_all(

        self,

    ):

        logger.info(

            "Loading all documents...",

        )

        documents = self.repo.get_all()

        return self.success(

            data=documents,

            count=len(

                documents,

            ),

        )

    def get(

        self,

        document_id,

    ):

        logger.info(

            "Loading document : %s",

            document_id,

        )

        document = self.repo.get(

            document_id,

        )

        if document is None:

            return self.error(

                "Document not found.",

            )

        return self.success(

            data=document,

            count=1,

        )

    def search(

        self,

        keyword,

    ):

        keyword = str(

            keyword or "",

        ).strip()

        if keyword == "":

            return self.error(

                "Keyword is required.",

            )

        logger.info(

            "Searching document : %s",

            keyword,

        )

        documents = self.repo.search(

            keyword,

        )

        return self.success(

            data=documents,

            count=len(

                documents,

            ),

            keyword=keyword,

        )

    # ==========================================================
    # Import Logs
    # ==========================================================

    def import_logs(

        self,

    ):

        logger.info(

            "Loading import logs...",

        )

        if not hasattr(

            self.repo,

            "import_logs",

        ):

            return self.error(

                "Repository does not support import logs.",

            )

        logs = self.repo.import_logs()

        return self.success(

            data=logs,

            count=len(

                logs,

            ),

        )

    # ==========================================================
    # Create
    # ==========================================================

    def create(

        self,

        data,

    ):

        logger.info(

            "Creating document...",

        )

        filename = self.validate_filename(

            data.get(

                "filename",

            )

        )

        content = str(

            data.get(

                "content",

                "",

            )

        )

        data["filename"] = filename

        data["file_hash"] = data.get(

            "file_hash",

        ) or self.build_hash(

            filename,

            content,

        )

        document_id = self.repo.create(

            data,

        )

        logger.info(

            "Document created : %s",

            document_id,

        )

        self.rebuild_vector()

        return self.success(

            message="Document created successfully.",

            data={

                "document_id": document_id,

            },

            count=1,

        )

    # ==========================================================
    # Import PDF
    # ==========================================================

    def import_pdf(

        self,

        files,

        form,

    ):

        logger.info(

            "Import PDF started.",

        )

        try:

            file = files.get(

                "file",

            )

            filename = self.validate_upload(

                file,

            )

        except ValueError as e:

            return self.error(

                str(

                    e,

                )

            )

        category = str(

            form.get(

                "category",

                "manual",

            )

        ).strip()

        model = str(

            form.get(

                "machine_model",

                "",

            )

        ).strip()

        filepath = self.upload_path / filename

        file.save(

            filepath,

        )

        logger.info(

            "PDF saved : %s",

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

        self.rebuild_vector()

        logger.info(

            "Imported %s pages.",

            pages,

        )

        return self.success(

            message="PDF imported successfully.",

            data={

                "filename": filename,

                "pages": pages,

                "category": category,

                "model": model,

            },

            count=pages,

        )

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

                "Document not found.",

            )

        filename = self.validate_filename(

            data.get(

                "filename",

                document.get(

                    "filename",

                    "",

                ),

            )

        )

        content = str(

            data.get(

                "content",

                document.get(

                    "content",

                    "",

                ),

            )

        )

        data["filename"] = filename

        data["file_hash"] = self.build_hash(

            filename,

            content,

        )

        self.repo.update(

            document_id,

            data,

        )

        self.rebuild_vector()

        logger.info(

            "Document updated : %s",

            document_id,

        )

        return self.success(

            message="Document updated successfully.",

            data={

                "document_id": document_id,

            },

            count=1,

        )
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

                "Document not found.",

            )

        self.repo.delete(

            document_id,

        )

        self.rebuild_vector()

        logger.info(

            "Document deleted : %s",

            document_id,

        )

        return self.success(

            message="Document deleted successfully.",

            data={

                "document_id": document_id,

            },

            count=1,

        )

    # ==========================================================
    # Latest Documents
    # ==========================================================

    def latest(

        self,

        limit=20,

    ):

        logger.info(

            "Loading latest documents...",

        )

        limit = max(

            1,

            int(

                limit,

            ),

        )

        if hasattr(

            self.repo,

            "latest",

        ):

            documents = self.repo.latest(

                limit,

            )

        else:

            documents = self.repo.get_all()[:limit]

        return self.success(

            data=documents,

            count=len(

                documents,

            ),

        )

    # ==========================================================
    # Total Documents
    # ==========================================================

    def total(

        self,

    ):

        logger.info(

            "Counting documents...",

        )

        if hasattr(

            self.repo,

            "total",

        ):

            total = self.repo.total()

        else:

            total = len(

                self.repo.get_all(),

            )

        return self.success(

            data={

                "total": total,

            },

            count=total,

        )

    # ==========================================================
    # Rebuild Embedding
    # ==========================================================

    def rebuild_embedding(

        self,

    ):

        logger.info(

            "Rebuilding embedding database...",

        )

        try:

            pages = self.rebuild_vector()

            return self.success(

                message="Vector database rebuilt successfully.",

                data={

                    "pages": pages,

                },

                count=pages,

            )

        except Exception as e:

            logger.exception(

                "Vector rebuild failed : %s",

                e,

            )

            return self.error(

                "Vector rebuild failed.",

            )
    # ==========================================================
    # PDF Path
    # ==========================================================

    def pdf_path(

        self,

        filename,

    ):

        filename = self.validate_filename(

            filename,

        )

        pdf = self.upload_path / filename

        if not pdf.is_file():

            logger.warning(

                "PDF not found : %s",

                pdf,

            )

            raise FileNotFoundError(

                filename,

            )

        return pdf

    # ==========================================================
    # View PDF
    # ==========================================================

    def view_pdf(

        self,

        filename,

    ):

        logger.info(

            "Viewing PDF : %s",

            filename,

        )

        pdf = self.pdf_path(

            filename,

        )

        return send_file(

            pdf,

            mimetype="application/pdf",

            as_attachment=False,

            download_name=pdf.name,

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

        pdf = self.pdf_path(

            filename,

        )

        return send_file(

            pdf,

            mimetype="application/pdf",

            as_attachment=True,

            download_name=pdf.name,

        )

    # ==========================================================
    # PDF Exists
    # ==========================================================

    def exists(

        self,

        filename,

    ):

        try:

            self.pdf_path(

                filename,

            )

            return True

        except FileNotFoundError:

            return False

    # ==========================================================
    # PDF Size
    # ==========================================================

    def file_size(

        self,

        filename,

    ):

        pdf = self.pdf_path(

            filename,

        )

        return pdf.stat().st_size

    # ==========================================================
    # PDF Information
    # ==========================================================

    def pdf_info(

        self,

        filename,

    ):

        pdf = self.pdf_path(

            filename,

        )

        return self.success(

            data={

                "filename": pdf.name,

                "path": str(

                    pdf,

                ),

                "size": pdf.stat().st_size,

                "exists": True,

            },

            count=1,

        )
    # ==========================================================
    # Health
    # ==========================================================

    def health(

        self,

    ):

        logger.info(

            "Document Service Health Check",

        )

        return {

            "success": True,

            "service": "document_service",

            "repository": self.repo is not None,

            "upload_folder": str(

                self.upload_path,

            ),

            "upload_exists": self.upload_path.exists(),

            "embedding_ready": embedding_service is not None,

            "rag_ready": rag_service.is_ready(),

            "status": "ok",

        }

    # ==========================================================
    # Statistics
    # ==========================================================

    def statistics(

        self,

    ):

        logger.info(

            "Loading document statistics...",

        )

        try:

            total = 0

            if hasattr(

                self.repo,

                "total",

            ):

                total = self.repo.total()

            else:

                total = len(

                    self.repo.get_all(),

                )

            return {

                "success": True,

                "total_documents": total,

                "upload_folder": str(

                    self.upload_path,

                ),

                "vector_ready": rag_service.is_ready(),

                "embedding_ready": embedding_service is not None,

            }

        except Exception as e:

            logger.exception(

                "Statistics Error : %s",

                e,

            )

            return self.error(

                "Unable to load statistics.",

            )

    # ==========================================================
    # Ready
    # ==========================================================

    def is_ready(

        self,

    ):

        return (

            self.upload_path.exists()

            and

            rag_service.is_ready()

        )

    # ==========================================================
    # Version
    # ==========================================================

    def version(

        self,

    ):

        return {

            "name": "LaundryBot V7 Enterprise",

            "module": "Document Service",

            "version": getattr(

                Config,

                "VERSION",

                "7.0",

            ),

            "upload_folder": str(

                self.upload_path,

            ),

        }


# ==========================================================
# Singleton
# ==========================================================

document_service = DocumentService()