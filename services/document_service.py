"""
LaundryBot V7 Enterprise
Document Service
"""

import os
import uuid

from werkzeug.utils import secure_filename

from repositories.document_repository import document_repository


class DocumentService:

    ALLOWED_EXTENSIONS = {"pdf"}

    def allowed_file(self, filename):

        return (
            "." in filename
            and filename.rsplit(".", 1)[1].lower()
            in self.ALLOWED_EXTENSIONS
        )

    def upload(
        self,
        file,
        category,
        title=None,
        machine_model=None,
        repair_id=None,
        uploaded_by=None,
    ):

        if file is None:
            raise Exception("No file selected")

        if file.filename == "":
            raise Exception("No filename")

        if not self.allowed_file(file.filename):
            raise Exception("Only PDF files are allowed")

        filename = secure_filename(file.filename)

        ext = filename.rsplit(".", 1)[1].lower()

        unique_name = f"{uuid.uuid4()}.{ext}"

        folder = os.path.join("uploads", category)

        os.makedirs(folder, exist_ok=True)

        filepath = os.path.join(folder, unique_name)

        file.save(filepath)

        filesize = os.path.getsize(filepath)

        document_repository.create(
            filename=filename,
            filepath=filepath,
            document_type="pdf",
            model=machine_model,
            category=category,
            filesize=filesize,
            uploaded_by=uploaded_by,
        )

        return filepath

    def get_all(self):
        return document_repository.get_all()

    def get(self, document_id):
        return document_repository.get(document_id)

    def delete(self, document_id):
        return document_repository.delete(document_id)


document_service = DocumentService()