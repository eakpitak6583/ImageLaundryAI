"""
LaundryBot V7 Enterprise
RAG Service
"""

import logging
from datetime import (
    datetime,
)
from pathlib import (
    Path,
)

from langchain_community.vectorstores import (
    FAISS,
)

from openai import (
    OpenAI,
)

from config import (
    Config,
)

from services.embedding_service import (
    embedding_service,
)

from services.prompt_service import (
    prompt_service,
)

logger = logging.getLogger(
    __name__,
)


class RagService:

    # ==========================================================
    # Constructor
    # ==========================================================

    def __init__(

        self,

    ):

        if not Config.OPENAI_API_KEY:

            raise RuntimeError(

                "OPENAI_API_KEY is missing."

            )

        self.client = OpenAI(

            api_key=Config.OPENAI_API_KEY,

        )

        self.vector_db = None

        self.vector_path = Path(

            Config.VECTOR_DB,

        ).resolve()

        logger.info(

            "RAG Service Initialized"

        )

    # ==========================================================
    # Empty Result
    # ==========================================================

    def empty_result(

        self,

        question="",

        message="ไม่พบข้อมูลในฐานความรู้",

    ):

        return {

            "success": False,

            "answer": message,

            "sources": [],

            "search_keyword": question,

            "count": 0,

            "model": Config.MODEL_NAME,

            "timestamp": datetime.now().isoformat(),

        }

    # ==========================================================
    # Health
    # ==========================================================

    def health(

        self,

    ):

        index = self.vector_path / "index.faiss"

        return {

            "success": True,

            "service": "rag_service",

            "vector_loaded": (

                self.vector_db is not None

            ),

            "vector_exists": index.exists(),

            "vector_path": str(

                self.vector_path,

            ),

            "model": Config.MODEL_NAME,

            "status": "ok",

        }
    # ==========================================================
    # Load Vector Database
    # ==========================================================

    def load(

        self,

    ):

        if self.vector_db is not None:

            logger.info(

                "Using cached vector database."

            )

            return self.vector_db

        index = self.vector_path / "index.faiss"

        if not index.exists():

            logger.warning(

                "Vector database not found : %s",

                index,

            )

            return None

        try:

            logger.info(

                "Loading vector database..."

            )

            self.vector_db = FAISS.load_local(

                str(

                    self.vector_path,

                ),

                embedding_service.embeddings,

                allow_dangerous_deserialization=True,

            )

            logger.info(

                "Vector database loaded successfully."

            )

            return self.vector_db

        except Exception as e:

            logger.exception(

                "Unable to load vector database: %s",

                e,

            )

            raise

    # ==========================================================
    # Search
    # ==========================================================

    def search(

        self,

        question,

        top_k=5,

    ):

        question = str(

            question or "",

        ).strip()

        if question == "":

            return {

                "success": False,

                "context": "",

                "sources": [],

                "count": 0,

            }

        logger.info(

            "Similarity Search : %s",

            question,

        )

        db = self.load()

        if db is None:

            return {

                "success": False,

                "context": "",

                "sources": [],

                "count": 0,

            }

        try:

            documents = db.similarity_search(

                question,

                k=top_k,

            )

        except Exception as e:

            logger.exception(

                "Similarity search failed: %s",

                e,

            )

            raise

        if not documents:

            return {

                "success": True,

                "context": "",

                "sources": [],

                "count": 0,

            }

        context = []

        sources = []

        for index, document in enumerate(

            documents,

            start=1,

        ):

            filename = document.metadata.get(

                "filename",

                "Unknown",

            )

            page = document.metadata.get(

                "page",

                "-",

            )

            content = str(

                document.page_content or "",

            ).strip()

            if not content:

                continue

            context.append(

                f"""

[{index}]

FILE : {filename}

PAGE : {page}

{content}

"""

            )

            sources.append(

                {

                    "filename": filename,

                    "page": page,

                    "content": content[:300],

                }

            )

        logger.info(

            "Retrieved %s document(s).",

            len(

                sources,

            ),

        )

        return {

            "success": True,

            "context": "\n".join(

                context,

            ),

            "sources": sources,

            "count": len(

                sources,

            ),

        }
    # ==========================================================
    # Ask AI
    # ==========================================================

    def ask(

        self,

        question,

        top_k=5,

    ):

        question = str(

            question or "",

        ).strip()

        if question == "":

            return self.empty_result(

                message="กรุณาระบุคำถาม",

            )

        logger.info(

            "AI Question : %s",

            question,

        )

        search_result = self.search(

            question,

            top_k,

        )

        if not search_result.get(

            "success",

        ):

            return self.empty_result(

                question,

            )

        knowledge = search_result.get(

            "context",

            "",

        )

        sources = search_result.get(

            "sources",

            [],

        )

        if knowledge == "":

            logger.info(

                "No knowledge found."

            )

            return self.empty_result(

                question,

            )

        prompt = prompt_service.rag_prompt(

            knowledge=knowledge,

            question=question,

        )

        try:

            response = self.client.responses.create(

                model=Config.MODEL_NAME,

                input=prompt,

            )

            answer = getattr(

                response,

                "output_text",

                "",

            ).strip()

            if answer == "":

                answer = "ไม่พบข้อมูลในฐานความรู้"

            logger.info(

                "AI response generated successfully."

            )

            return {

                "success": True,

                "answer": answer,

                "sources": sources,

                "search_keyword": question,

                "count": len(

                    sources,

                ),

                "model": Config.MODEL_NAME,

                "timestamp": datetime.now().isoformat(),

            }

        except Exception as e:

            logger.exception(

                "OpenAI request failed: %s",

                e,

            )

            return {

                "success": False,

                "answer": "",

                "message": str(

                    e,

                ),

                "sources": [],

                "search_keyword": question,

                "count": 0,

                "model": Config.MODEL_NAME,

                "timestamp": datetime.now().isoformat(),

            }

    # ==========================================================
    # Ask JSON
    # ==========================================================

    def ask_json(

        self,

        question,

        top_k=5,

    ):

        return self.ask(

            question,

            top_k,

        )
    # ==========================================================
    # Build Query
    # ==========================================================

    def build_query(

        self,

        **kwargs,

    ):

        sections = []

        for title, value in kwargs.items():

            value = str(

                value or "",

            ).strip()

            if not value:

                continue

            sections.append(

                f"{title}\n\n{value}"

            )

        return "\n\n".join(

            sections,

        )

    # ==========================================================
    # Ask Machine
    # ==========================================================

    def ask_machine(

        self,

        machine,

        symptom,

        top_k=5,

    ):

        logger.info(

            "Machine Question : %s | %s",

            machine,

            symptom,

        )

        query = self.build_query(

            Machine=machine,

            Problem=symptom,

        )

        return self.ask(

            query,

            top_k,

        )

    # ==========================================================
    # Ask Manual
    # ==========================================================

    def ask_manual(

        self,

        machine,

        keyword,

        top_k=5,

    ):

        logger.info(

            "Manual Search : %s | %s",

            machine,

            keyword,

        )

        query = self.build_query(

            Machine=machine,

            Keyword=keyword,

        )

        return self.ask(

            query,

            top_k,

        )

    # ==========================================================
    # Ask Repair
    # ==========================================================

    def ask_repair(

        self,

        machine,

        error_code,

        symptom,

        top_k=5,

    ):

        logger.info(

            "Repair Question : %s",

            machine,

        )

        query = self.build_query(

            Machine=machine,

            Error_Code=error_code,

            Symptom=symptom,

        )

        return self.ask(

            query,

            top_k,

        )

    # ==========================================================
    # Search JSON
    # ==========================================================

    def search_json(

        self,

        question,

        top_k=5,

    ):

        return self.search(

            question,

            top_k,

        )
    # ==========================================================
    # Clear Cache
    # ==========================================================

    def clear_cache(

        self,

    ):

        logger.info(

            "Clearing vector database cache."

        )

        self.vector_db = None

    # ==========================================================
    # Reload Vector Database
    # ==========================================================

    def reload(

        self,

    ):

        logger.info(

            "Reloading vector database."

        )

        self.clear_cache()

        return self.load()

    # ==========================================================
    # Statistics
    # ==========================================================

    def statistics(

        self,

    ):

        index = self.vector_path / "index.faiss"

        return {

            "vector_loaded": (

                self.vector_db is not None

            ),

            "vector_exists": index.exists(),

            "vector_path": str(

                self.vector_path,

            ),

            "model": Config.MODEL_NAME,

        }

    # ==========================================================
    # Version
    # ==========================================================

    def version(

        self,

    ):

        return {

            "name": "LaundryBot V7 Enterprise",

            "module": "RAG Service",

            "version": getattr(

                Config,

                "VERSION",

                "7.0",

            ),

            "model": Config.MODEL_NAME,

            "embedding_model": getattr(

                Config,

                "EMBEDDING_MODEL",

                "text-embedding-3-small",

            ),

        }

    # ==========================================================
    # Ready
    # ==========================================================

    def is_ready(

        self,

    ):

        index = self.vector_path / "index.faiss"

        return (

            bool(

                Config.OPENAI_API_KEY,

            )

            and index.exists()

        )


# ==========================================================
# Singleton
# ==========================================================

rag_service = RagService()
