"""
LaundryBot V7 Enterprise
AI Routes
"""

import logging

from flask import (
    Blueprint,
    jsonify,
    render_template,
    request,
)

from flask_login import (
    login_required,
)

from services.rag_service import (
    rag_service,
)

logger = logging.getLogger(
    __name__,
)

ai_bp = Blueprint(

    "ai",

    __name__,

    url_prefix="/ai",

)


# ==========================================================
# AI Chat Page
# ==========================================================

@ai_bp.route(

    "/",

)

@login_required

def index():

    return render_template(

        "ai_chat.html",

    )
# ==========================================================
# AI Chat API
# ==========================================================

@ai_bp.route(

    "/chat",

    methods=[

        "POST",

    ],

)

@login_required

def chat():

    try:

        payload = request.get_json(

            silent=True,

        ) or {}

        question = str(

            payload.get(

                "question",

                "",

            )

        ).strip()

        if question == "":

            return jsonify(

                rag_service.empty_result(

                    message="กรุณาพิมพ์คำถาม",

                )

            ), 400

        logger.info(

            "AI Chat : %s",

            question,

        )

        return jsonify(

            rag_service.ask(

                question,

            )

        )

    except Exception as e:

        logger.exception(

            "AI Chat Error : %s",

            e,

        )

        return jsonify({

            "success": False,

            "answer": "",

            "message": str(

                e,

            ),

            "sources": [],

            "search_keyword": "",

            "count": 0,

        }), 500
# ==========================================================
# Health Check
# ==========================================================

@ai_bp.route(

    "/health",

)

@login_required

def health():

    return jsonify(

        rag_service.health(),

    )
# ==========================================================
# Search API
# ==========================================================

@ai_bp.route(

    "/search",

    methods=[

        "POST",

    ],

)

@login_required

def search():

    try:

        payload = request.get_json(

            silent=True,

        ) or {}

        keyword = str(

            payload.get(

                "question",

                "",

            )

        ).strip()

        if keyword == "":

            return jsonify({

                "success": False,

                "message": "Keyword is required",

                "sources": [],

                "count": 0,

            }), 400

        logger.info(

            "AI Search : %s",

            keyword,

        )

        return jsonify(

            rag_service.search_json(

                keyword,

            )

        )

    except Exception as e:

        logger.exception(

            "AI Search Error : %s",

            e,

        )

        return jsonify({

            "success": False,

            "message": str(

                e,

            ),

            "sources": [],

            "count": 0,

        }), 500
# ==========================================================
# Version
# ==========================================================

@ai_bp.route(

    "/version",

)

@login_required

def version():

    return jsonify(

        rag_service.version(),

    )


# ==========================================================
# Statistics
# ==========================================================

@ai_bp.route(

    "/statistics",

)

@login_required

def statistics():

    return jsonify(

        rag_service.statistics(),

    )


# ==========================================================
# Ready
# ==========================================================

@ai_bp.route(

    "/ready",

)

@login_required

def ready():

    return jsonify({

        "success": True,

        "ready": rag_service.is_ready(),

    })


# ==========================================================
# Reload Vector
# ==========================================================

@ai_bp.route(

    "/reload",

    methods=[

        "POST",

    ],

)

@login_required

def reload():

    try:

        rag_service.reload()

        return jsonify({

            "success": True,

            "message": "Vector database reloaded successfully.",

        })

    except Exception as e:

        logger.exception(

            "Reload Vector Error : %s",

            e,

        )

        return jsonify({

            "success": False,

            "message": str(

                e,

            ),

        }), 500
# ==========================================================
# Clear Vector Cache
# ==========================================================

@ai_bp.route(

    "/clear-cache",

    methods=[

        "POST",

    ],

)

@login_required

def clear_cache():

    try:

        rag_service.clear_cache()

        return jsonify({

            "success": True,

            "message": "Vector cache cleared.",

        })

    except Exception as e:

        logger.exception(

            "Clear Cache Error : %s",

            e,

        )

        return jsonify({

            "success": False,

            "message": str(

                e,

            ),

        }), 500


# ==========================================================
# AI Information
# ==========================================================

@ai_bp.route(

    "/info",

)

@login_required

def info():

    return jsonify({

        "success": True,

        "health": rag_service.health(),

        "version": rag_service.version(),

        "statistics": rag_service.statistics(),

        "ready": rag_service.is_ready(),

    })


# ==========================================================
# Ping
# ==========================================================

@ai_bp.route(

    "/ping",

)

def ping():

    return jsonify({

        "success": True,

        "service": "LaundryBot AI",

    })
# ==========================================================
# AI Status
# ==========================================================

@ai_bp.route(

    "/status",

)

@login_required

def status():

    return jsonify({

        "success": True,

        "service": "LaundryBot AI",

        "health": rag_service.health(),

        "statistics": rag_service.statistics(),

        "version": rag_service.version(),

        "ready": rag_service.is_ready(),

    })


# ==========================================================
# Warmup
# ==========================================================

@ai_bp.route(

    "/warmup",

    methods=[

        "POST",

    ],

)

@login_required

def warmup():

    try:

        rag_service.load()

        return jsonify({

            "success": True,

            "message": "Vector database loaded.",

        })

    except Exception as e:

        logger.exception(

            "Warmup Error : %s",

            e,

        )

        return jsonify({

            "success": False,

            "message": str(

                e,

            ),

        }), 500


# ==========================================================
# Test AI
# ==========================================================

@ai_bp.route(

    "/test",

)

@login_required

def test():

    return jsonify({

        "success": True,

        "service": "LaundryBot AI",

        "model": Config.MODEL_NAME,

        "vector_ready": rag_service.is_ready(),

    })