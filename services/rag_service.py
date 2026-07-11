"""
LaundryBot V7 Enterprise
RAG Service
"""

import logging
from pathlib import Path

from openai import (
    OpenAI,
)

from langchain_community.vectorstores import (
    FAISS,
)

from config import (
    Config,
)

from services.embedding_service import (
    embedding_service,
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
    # Health
    # ==========================================================

    def health(

        self,

    ):

        return {

            "success": True,

            "service": "rag_service",

            "vector_path": str(

                self.vector_path,

            ),

            "vector_loaded": (

                self.vector_db is not None

            ),

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

                "Failed to load vector database: %s",

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

            logger.warning(

                "Empty search question."

            )

            return {

                "success": False,

                "documents": [],

                "context": "",

                "count": 0,

            }

        logger.info(

            "Similarity Search : %s",

            question,

        )

        db = self.load()

        if db is None:

            logger.warning(

                "Vector database unavailable."

            )

            return {

                "success": False,

                "documents": [],

                "context": "",

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

            logger.info(

                "No related documents found."

            )

            return {

                "success": True,

                "documents": [],

                "context": "",

                "count": 0,

            }

        context = []

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

        logger.info(

            "Retrieved %s document(s).",

            len(

                documents,

            ),

        )

        return {

            "success": True,

            "documents": documents,

            "context": "\n".join(

                context,

            ),

            "count": len(

                documents,

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

            return "กรุณาระบุคำถาม"

        logger.info(

            "AI Question : %s",

            question,

        )

        knowledge = self.search(

            question,

            top_k,

        )

        if knowledge == "":

            logger.info(

                "No knowledge found."

            )

            return "ไม่พบข้อมูลในฐานความรู้"

        prompt = f"""
คุณคือ LaundryBot V7 Enterprise

หน้าที่ของคุณคือผู้ช่วยวิศวกรซ่อมเครื่องซักผ้าอุตสาหกรรม

ให้ตอบโดยอ้างอิงจากข้อมูลในฐานความรู้ด้านล่างเท่านั้น

==========================
KNOWLEDGE
==========================

{knowledge}

==========================
QUESTION
==========================

{question}

==========================
RULES
==========================

1. ตอบเฉพาะข้อมูลที่อยู่ใน KNOWLEDGE

2. หากไม่มีข้อมูลเพียงพอ ให้ตอบว่า

"ไม่พบข้อมูลในฐานความรู้"

3. ห้ามเดา

4. หากอ้างอิงเอกสาร ให้ระบุ FILE และ PAGE ที่เกี่ยวข้อง

ตอบเป็นภาษาไทย
"""

        try:

            response = self.client.responses.create(

                model=Config.MODEL_NAME,

                input=prompt,

            )

            answer = response.output_text.strip()

            logger.info(

                "AI response generated successfully."

            )

            return answer

        except Exception as e:

            logger.exception(

                "OpenAI request failed: %s",

                e,

            )

            raise
    # ==========================================================
    # Ask Machine
    # ==========================================================

    def ask_machine(

        self,

        machine,

        symptom,

        top_k=5,

    ):

        machine = str(

            machine or "",

        ).strip()

        symptom = str(

            symptom or "",

        ).strip()

        logger.info(

            "Machine Question : %s | %s",

            machine,

            symptom,

        )

        query = f"""

Machine

{machine}

Problem

{symptom}

"""

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

        machine = str(

            machine or "",

        ).strip()

        keyword = str(

            keyword or "",

        ).strip()

        logger.info(

            "Manual Search : %s | %s",

            machine,

            keyword,

        )

        query = f"""

Machine

{machine}

Keyword

{keyword}

"""

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

        machine = str(

            machine or "",

        ).strip()

        error_code = str(

            error_code or "",

        ).strip()

        symptom = str(

            symptom or "",

        ).strip()

        logger.info(

            "Repair Question : %s",

            machine,

        )

        query = f"""

Machine

{machine}

Error Code

{error_code}

Symptom

{symptom}

"""

        return self.ask(

            query,

            top_k,

        )

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

        }
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

        return {

            "vector_loaded": (

                self.vector_db is not None

            ),

            "vector_path": str(

                self.vector_path,

            ),

            "model": Config.MODEL_NAME,

        }


# ==========================================================
# Singleton
# ==========================================================

rag_service = RagService()