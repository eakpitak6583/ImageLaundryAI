"""
Image Laundry AI
Document Service
"""

import hashlib

from repositories.document_repository import (
    document_repository,
)

from services.base_service import BaseService


class DocumentService(BaseService):

    # ==========================================================
    # Read
    # ==========================================================

    def get_all(self):

        return document_repository.get_all()

    def get(self, document_id):

        return document_repository.get(document_id)

    def search(self, keyword):

        return document_repository.search(keyword)

    # ==========================================================
    # Create
    # ==========================================================

    def create(self, data):

        if not data.get("filename"):

            return self.error(
                "Filename is required"
            )

        file_hash = data.get("file_hash")

        if not file_hash:

            content = data.get("content", "")

            file_hash = hashlib.sha256(
                content.encode("utf-8")
            ).hexdigest()

            data["file_hash"] = file_hash

        document_id = document_repository.create(
            data
        )

        return self.success(document_id)

    # ==========================================================
    # Update
    # ==========================================================

    def update(self, document_id, data):

        document = document_repository.get(
            document_id
        )

        if not document:

            return self.error(
                "Document not found"
            )

        document_repository.update(
            document_id,
            data,
        )

        return self.success()

    # ==========================================================
    # Delete
    # ==========================================================

    def delete(self, document_id):

        document = document_repository.get(
            document_id
        )

        if not document:

            return self.error(
                "Document not found"
            )

        document_repository.delete(
            document_id
        )

        return self.success()


document_service = DocumentService()