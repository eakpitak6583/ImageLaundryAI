"""
LaundryBot V7 Enterprise
Document Routes
"""

import logging

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
)

from flask_login import (
    login_required,
)

from services.document_service import (
    document_service,
)

logger = logging.getLogger(
    __name__,
)

documents_bp = Blueprint(
    "documents",
    __name__,
    url_prefix="/documents",
)


# ==========================================================
# Document Home
# ==========================================================

@documents_bp.route(
    "/",
    methods=[
        "GET",
    ],
)
@login_required
def index():

    logger.info(
        "Loading document dashboard..."
    )

    try:

        logs = document_service.import_logs()

    except Exception as e:

        logger.exception(e)

        flash(
            "Unable to load document list.",
            "danger",
        )

        logs = []

    return render_template(

        "documents.html",

        logs=logs,

    )
# ==========================================================
# Upload PDF
# ==========================================================

@documents_bp.route(
    "/upload",
    methods=[
        "POST",
    ],
)
@login_required
def upload():

    logger.info(
        "Document upload started."
    )

    try:

        result = document_service.import_pdf(

            request.files,

            request.form,

        )

        if not result.get(

            "success",

        ):

            flash(

                result.get(

                    "message",

                    "Import failed.",

                ),

                "warning",

            )

            return redirect(

                url_for(

                    "documents.index",

                )

            )

        flash(

            f"Import completed ({result['pages']} pages).",

            "success",

        )

        logger.info(

            "Imported %s pages.",

            result["pages"],

        )

    except Exception as e:

        logger.exception(e)

        flash(

            "Import failed.",

            "danger",

        )

    return redirect(

        url_for(

            "documents.index",

        )

    )
# ==========================================================
# Search Document
# ==========================================================

@documents_bp.route(
    "/search",
    methods=[
        "GET",
    ],
)
@login_required
def search():

    keyword = request.args.get(
        "q",
        "",
    ).strip()

    logger.info(

        "Document Search : %s",

        keyword,

    )

    try:

        if keyword:

            rows = document_service.search(

                keyword,

            )

        else:

            rows = []

    except Exception as e:

        logger.exception(e)

        flash(

            "Unable to search documents.",

            "danger",

        )

        rows = []

    return render_template(

        "document_search.html",

        keyword=keyword,

        rows=rows,

    )


# ==========================================================
# Rebuild Vector Database
# ==========================================================

@documents_bp.route(
    "/rebuild",
    methods=[
        "POST",
    ],
)
@login_required
def rebuild():

    logger.info(

        "Rebuilding embedding database..."

    )

    try:

        result = document_service.rebuild_embedding()

        if not result.get(

            "success",

        ):

            flash(

                result.get(

                    "message",

                    "Vector rebuild failed.",

                ),

                "warning",

            )

            return redirect(

                url_for(

                    "documents.index",

                )

            )

        flash(

            f"Vector rebuilt successfully ({result['pages']} pages).",

            "success",

        )

        logger.info(

            "Embedding rebuilt : %s pages",

            result["pages"],

        )

    except Exception as e:

        logger.exception(e)

        flash(

            "Vector rebuild failed.",

            "danger",

        )

    return redirect(

        url_for(

            "documents.index",

        )

    )
# ==========================================================
# PDF Viewer
# ==========================================================

@documents_bp.route(
    "/viewer",
    methods=[
        "GET",
    ],
)
@login_required
def viewer():

    filename = request.args.get(

        "file",

        "",

    ).strip()

    page = request.args.get(

        "page",

        1,

        type=int,

    )

    if filename == "":

        flash(

            "Document not found.",

            "warning",

        )

        return redirect(

            url_for(

                "documents.index",

            )

        )

    logger.info(

        "Open PDF Viewer : %s (page %s)",

        filename,

        page,

    )

    return render_template(

        "pdf_viewer.html",

        filename=filename,

        page=page,

    )


# ==========================================================
# Stream PDF
# ==========================================================

@documents_bp.route(
    "/view",
    methods=[
        "GET",
    ],
)
@login_required
def view_pdf():

    filename = request.args.get(

        "file",

        "",

    ).strip()

    if filename == "":

        flash(

            "Document not found.",

            "warning",

        )

        return redirect(

            url_for(

                "documents.index",

            )

        )

    logger.info(

        "Open PDF : %s",

        filename,

    )

    try:

        return document_service.view_pdf(

            filename,

        )

    except FileNotFoundError:

        flash(

            "PDF file not found.",

            "warning",

        )

    except Exception as e:

        logger.exception(e)

        flash(

            "Unable to open PDF.",

            "danger",

        )

    return redirect(

        url_for(

            "documents.index",

        )

    )
# ==========================================================
# Download PDF
# ==========================================================

@documents_bp.route(
    "/download",
    methods=[
        "GET",
    ],
)
@login_required
def download():

    filename = request.args.get(

        "file",

        "",

    ).strip()

    if filename == "":

        flash(

            "Document not found.",

            "warning",

        )

        return redirect(

            url_for(

                "documents.index",

            )

        )

    logger.info(

        "Download PDF : %s",

        filename,

    )

    try:

        return document_service.download_pdf(

            filename,

        )

    except FileNotFoundError:

        flash(

            "PDF file not found.",

            "warning",

        )

    except Exception as e:

        logger.exception(e)

        flash(

            "Unable to download PDF.",

            "danger",

        )

    return redirect(

        url_for(

            "documents.index",

        )

    )


# ==========================================================
# Delete Document
# ==========================================================

@documents_bp.route(
    "/delete/<int:document_id>",
    methods=[
        "POST",
    ],
)
@login_required
def delete(

    document_id,

):

    logger.info(

        "Delete document : %s",

        document_id,

    )

    try:

        result = document_service.delete(

            document_id,

        )

        if result.get(

            "success",

        ):

            flash(

                "Document deleted successfully.",

                "success",

            )

        else:

            flash(

                result.get(

                    "message",

                    "Unable to delete document.",

                ),

                "warning",

            )

    except Exception as e:

        logger.exception(e)

        flash(

            "Delete failed.",

            "danger",

        )

    return redirect(

        url_for(

            "documents.index",

        )

    )
# ==========================================================
# 404 Error
# ==========================================================

@documents_bp.errorhandler(
    404,
)
def not_found(
    error,
):

    logger.warning(

        "404 : %s",

        error,

    )

    flash(

        "Document page not found.",

        "warning",

    )

    return redirect(

        url_for(

            "documents.index",

        )

    )


# ==========================================================
# 500 Error
# ==========================================================

@documents_bp.errorhandler(
    500,
)
def internal_error(
    error,
):

    logger.exception(

        error,

    )

    flash(

        "Internal Server Error.",

        "danger",

    )

    return redirect(

        url_for(

            "documents.index",

        )

    )


# ==========================================================
# Health Check
# ==========================================================

@documents_bp.route(
    "/health",
    methods=[
        "GET",
    ],
)
@login_required
def health():

    logger.info(

        "Document module health check."

    )

    return {

        "success": True,

        "module": "documents",

        "status": "ok",

    }


# ==========================================================
# End of File
# ==========================================================