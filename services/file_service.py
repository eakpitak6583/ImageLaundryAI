"""
LaundryBot V7 Enterprise
File Upload Service
"""

from pathlib import Path
from uuid import uuid4


class FileService:

    def save(self, file, folder):

        if file is None:
            return None

        if file.filename == "":
            return None

        folder.mkdir(
            parents=True,
            exist_ok=True,
        )

        ext = Path(file.filename).suffix.lower()

        filename = f"{uuid4().hex}{ext}"

        filepath = folder / filename

        file.save(filepath)

        return filename

    def remove(self, folder, filename):

        if not filename:
            return

        path = folder / filename

        if path.exists():
            path.unlink()


file_service = FileService()