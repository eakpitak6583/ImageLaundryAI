"""
Image Laundry AI
Document Service
"""

import hashlib
import logging

from repositories.document_repository import (
    document_repository,
)

from services.base_service import (
    BaseService,
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

        return self.repo.latest(

            limit,

        )

    # ==========================================================
    # Statistics
    # ==========================================================

    def total(

        self,

    ):

        return self.repo.total()


# ==========================================================
# Singleton
# ==========================================================

document_service = DocumentService()
