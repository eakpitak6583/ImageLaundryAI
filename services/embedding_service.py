"""
LaundryBot V7 Enterprise
Embedding Service
"""

import logging
from pathlib import Path

from langchain_core.documents import (
    Document,
)

from langchain_community.vectorstores import (
    FAISS,
)

from langchain_openai import (
    OpenAIEmbeddings,
)

from config import (
    Config,
)

from database.db import (
    connect,
)

logger = logging.getLogger(

    __name__,

)


class EmbeddingService:

    # ==========================================================
    # Constructor
    # ==========================================================

    def __init__(

        self,

    ):

        self.vector_path = Path(

            Config.VECTOR_DB,

        ).resolve()

        self.vector_path.mkdir(

            parents=True,

            exist_ok=True,

        )

        self._embeddings = None

        logger.info(

            "Embedding Service Initialized"

        )

    # ==========================================================
    # OpenAI Embeddings
    # ==========================================================

    @property
    def embeddings(

        self,

    ):

        if self._embeddings is None:

            if not Config.OPENAI_API_KEY:

                raise RuntimeError(

                    "OPENAI_API_KEY is missing."

                )

            logger.info(

                "Initializing OpenAI Embeddings..."

            )

            self._embeddings = OpenAIEmbeddings(

                api_key=Config.OPENAI_API_KEY,

                model=getattr(

                    Config,

                    "EMBEDDING_MODEL",

                    "text-embedding-3-small",

                ),

            )

        return self._embeddings
    # ==========================================================
    # Build Vector Database
    # ==========================================================

    def build(

        self,

    ):

        logger.info(

            "Building vector database..."

        )

        conn = connect()

        try:

            rows = conn.execute(

                """

                SELECT

                    filename,

                    page,

                    content

                FROM documents

                ORDER BY

                    filename,

                    page

                """

            ).fetchall()

        finally:

            conn.close()

        if not rows:

            raise RuntimeError(

                "No document data found."

            )

        docs = []

        for row in rows:

            content = str(

                row["content"] or ""

            ).strip()

            if content == "":

                continue

            docs.append(

                Document(

                    page_content=content,

                    metadata={

                        "filename": row["filename"],

                        "page": row["page"],

                    },

                )

            )

        if not docs:

            raise RuntimeError(

                "No valid document content found."

            )

        logger.info(

            "Embedding %s pages...",

            len(docs),

        )

        try:

            db = FAISS.from_documents(

                docs,

                self.embeddings,

            )

            db.save_local(

                str(

                    self.vector_path,

                )

            )

        except Exception as e:

            logger.exception(

                "Failed to build vector database: %s",

                e,

            )

            raise

        logger.info(

            "Vector database created successfully."

        )

        return len(

            docs,

        )
    # ==========================================================
    # Load Vector Database
    # ==========================================================

    def load(

        self,

    ):

        logger.info(

            "Loading vector database..."

        )

        index = self.vector_path / "index.faiss"

        if not index.exists():

            logger.warning(

                "Vector database not found."

            )

            return None

        try:

            db = FAISS.load_local(

                str(

                    self.vector_path,

                ),

                self.embeddings,

                allow_dangerous_deserialization=True,

            )

            logger.info(

                "Vector database loaded successfully."

            )

            return db

        except Exception as e:

            logger.exception(

                "Unable to load vector database: %s",

                e,

            )

            raise
    # ==========================================================
    # Similarity Search
    # ==========================================================

    def similarity_search(

        self,

        question,

        k=5,

    ):

        question = str(

            question or "",

        ).strip()

        if question == "":

            logger.warning(

                "Similarity search called with empty question."

            )

            return []

        logger.info(

            "Similarity Search : %s",

            question,

        )

        db = self.load()

        if db is None:

            raise RuntimeError(

                "Vector database not found."

            )

        try:

            results = db.similarity_search(

                question,

                k=k,

            )

            logger.info(

                "Similarity search returned %s documents.",

                len(results),

            )

            return results

        except Exception as e:

            logger.exception(

                "Similarity search failed: %s",

                e,

            )

            raise
    # ==========================================================
    # Rebuild Vector Database
    # ==========================================================

    def rebuild(

        self,

    ):

        logger.info(

            "Rebuilding vector database..."

        )

        try:

            pages = self.build()

            logger.info(

                "Vector database rebuilt successfully (%s pages).",

                pages,

            )

            return pages

        except Exception as e:

            logger.exception(

                "Vector rebuild failed: %s",

                e,

            )

            raise
    # ==========================================================
    # Health
    # ==========================================================

    def health(

        self,

    ):

        logger.info(

            "Embedding Service Health Check"

        )

        return {

            "success": True,

            "service": "embedding_service",

            "status": "ok",

            "vector_path": str(

                self.vector_path,

            ),

        }

    # ==========================================================
    # Version
    # ==========================================================

    def version(

        self,

    ):

        return {

            "name": "LaundryBot V7 Enterprise",

            "module": "Embedding Service",

            "version": "7.0",

            "embedding_model": getattr(

                Config,

                "EMBEDDING_MODEL",

                "text-embedding-3-small",

            ),

        }


# ==========================================================
# Singleton
# ==========================================================

embedding_service = EmbeddingService()
