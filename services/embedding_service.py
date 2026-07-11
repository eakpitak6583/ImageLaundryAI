"""
LaundryBot V7 Enterprise
Embedding Service
"""

from pathlib import Path
import os

from config import Config
from database.db import connect

from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS


class EmbeddingService:

    def __init__(self):

        self.vector_path = str(Config.VECTOR_DB)

        Path(self.vector_path).mkdir(
            parents=True,
            exist_ok=True,
        )

        self._embeddings = None

    # ======================================================
    # OpenAI Embeddings
    # ======================================================

    @property
    def embeddings(self):

        if self._embeddings is None:

            print("=" * 60)
            print("CONFIG KEY :", Config.OPENAI_API_KEY)
            print("ENV KEY    :", os.getenv("OPENAI_API_KEY"))
            print("=" * 60)

            self._embeddings = OpenAIEmbeddings(
                api_key=Config.OPENAI_API_KEY,
                model="text-embedding-3-small",
            )

        return self._embeddings

    # ======================================================
    # Build Vector Database
    # ======================================================

    def build(self):

        conn = connect()

        rows = conn.execute(
            """
            SELECT
                filename,
                page,
                content
            FROM documents
            ORDER BY filename,page
            """
        ).fetchall()

        if not rows:
            raise RuntimeError("No document data found.")

        docs = []

        for row in rows:

            docs.append(
                Document(
                    page_content=row["content"],
                    metadata={
                        "filename": row["filename"],
                        "page": row["page"],
                    },
                )
            )

        db = FAISS.from_documents(
            docs,
            self.embeddings,
        )

        db.save_local(self.vector_path)

        return len(docs)

    # ======================================================
    # Load Vector
    # ======================================================

    def load(self):

        index = Path(self.vector_path) / "index.faiss"

        if not index.exists():
            return None

        return FAISS.load_local(
            self.vector_path,
            self.embeddings,
            allow_dangerous_deserialization=True,
        )

    # ======================================================
    # Search
    # ======================================================

    def similarity_search(
        self,
        question,
        k=5,
    ):

        db = self.load()

        if db is None:
            raise RuntimeError("Vector database not found.")

        return db.similarity_search(
            question,
            k=k,
        )

    # ======================================================
    # Rebuild
    # ======================================================

    def rebuild(self):

        return self.build()


embedding_service = EmbeddingService()