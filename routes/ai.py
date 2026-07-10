"""
LaundryBot V7 Enterprise
AI Routes
"""

import traceback
from datetime import datetime

from flask import (
    Blueprint,
    jsonify,
    render_template,
    request,
)

from flask_login import login_required

from config import Config
from services.rag_service import rag_service


ai_bp = Blueprint(
    "ai",
    __name__,
    url_prefix="/ai",
)


# ==========================================================
# AI Chat Page
# ==========================================================

@ai_bp.route("/")
@login_required
def index():

    return render_template(
        "ai_chat.html"
    )


# ==========================================================
# AI Chat API
# ==========================================================

@ai_bp.route(
    "/chat",
    methods=["POST"],
)
@login_required
def chat():

    try:

        payload = request.get_json(
            silent=True
        ) or {}

        question = payload.get(
            "question",
            ""
        ).strip()

        if not question:

            return jsonify({

                "success": False,

                "message": "กรุณาพิมพ์คำถาม",

                "answer": "",

                "sources": [],

                "count": 0,

                "search_keyword": "",

            }), 400

        result = rag_service.ask(question)

        answer = result.get(
            "answer",
            ""
        )

        sources = result.get(
            "sources",
            []
        )

        # ----------------------------------------------
        # Search Keyword
        # (รองรับ PDF Highlight ในอนาคต)
        # ----------------------------------------------

        search_keyword = result.get(
            "search_keyword",
            question
        )

        return jsonify({

            "success": True,

            "question": question,

            "search_keyword": search_keyword,

            "answer": answer,

            "sources": sources,

            "count": len(sources),

            "model": Config.MODEL_NAME,

            "service": "LaundryBot AI Enterprise",

            "timestamp": datetime.now().isoformat(),

        })

    except Exception as e:

        traceback.print_exc()

        return jsonify({

            "success": False,

            "message": str(e),

            "answer": "",

            "sources": [],

            "count": 0,

            "search_keyword": "",

        }), 500


# ==========================================================
# Health Check
# ==========================================================

@ai_bp.route("/health")
@login_required
def health():

    return jsonify({

        "success": True,

        "service": "LaundryBot AI Enterprise",

        "status": "ONLINE",

        "model": Config.MODEL_NAME,

        "rag": True,

        "embedding": True,

        "time": datetime.now().isoformat(),

    })


# ==========================================================
# Search API
# ==========================================================

@ai_bp.route(
    "/search",
    methods=["POST"],
)
@login_required
def search():

    try:

        payload = request.get_json(
            silent=True
        ) or {}

        keyword = payload.get(
            "question",
            ""
        ).strip()

        if not keyword:

            return jsonify({

                "success": False,

                "message": "Keyword is required",

                "count": 0,

                "results": []

            }), 400

        docs = rag_service.search(
            keyword
        )

        results = []

        for doc in docs:

            results.append({

                "filename": doc.metadata.get(
                    "filename",
                    ""
                ),

                "page": doc.metadata.get(
                    "page",
                    0
                ),

                "score": doc.metadata.get(
                    "score",
                    None
                ),

                "content": doc.page_content[:500],

            })

        return jsonify({

            "success": True,

            "keyword": keyword,

            "count": len(results),

            "results": results,

        })

    except Exception as e:

        traceback.print_exc()

        return jsonify({

            "success": False,

            "message": str(e),

            "count": 0,

            "results": []

        }), 500