"""
Image Laundry AI
Document Routes
"""

from pathlib import Path
import traceback

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    send_file,
    abort,
)

from flask_login import login_required

from config import Config
from database.db import connect

from services.pdf_service import pdf_service
from services.embedding_service import embedding_service


documents_bp = Blueprint(
    "documents",
    __name__,
    url_prefix="/documents",
)

UPLOAD_PATH = Path(Config.UPLOAD_FOLDER)


# ==========================================================
# Document Home
# ==========================================================

@documents_bp.route("/", methods=["GET"])
@login_required
def index():

    conn = connect()

    try:

        logs = conn.execute("""

            SELECT *

            FROM import_logs

            ORDER BY imported_at DESC

        """).fetchall()

    finally:

        conn.close()

    return render_template(

        "documents.html",

        logs=logs,

    )


# ==========================================================
# Upload PDF
# ==========================================================

@documents_bp.route(
    "/upload",
    methods=["POST"],
)
@login_required
def upload():

    try:

        file = request.files.get("file")

        if not file or file.filename == "":

            flash(
                "Please select a PDF file.",
                "warning",
            )

            return redirect(
                url_for(
                    "documents.index"
                )
            )

        category = request.form.get(
            "category",
            "manual",
        )

        model = request.form.get(
            "machine_model",
            "",
        )

        UPLOAD_PATH.mkdir(
            parents=True,
            exist_ok=True,
        )

        filename = Path(
            file.filename
        ).name

        filepath = UPLOAD_PATH / filename

        file.save(filepath)

        imported = pdf_service.import_pdf(

            filepath=str(filepath),

            filename=filename,

            document_type=category,

            model=model,

            category=category,

        )

        embedding_service.build()

        flash(

            f"Import completed ({imported} pages)",

            "success",

        )

    except Exception:

        traceback.print_exc()

        flash(

            "Import failed. See server log.",

            "danger",

        )

    return redirect(
        url_for(
            "documents.index"
        )
    )


# ==========================================================
# Search Document
# ==========================================================

@documents_bp.route(
    "/search",
    methods=["GET"],
)
@login_required
def search():

    keyword = request.args.get(
        "q",
        "",
    ).strip()

    rows = []

    if keyword:

        rows = pdf_service.search(
            keyword
        )

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
    methods=["GET"],
)
@login_required
def rebuild():

    try:

        pages = embedding_service.build()

        flash(

            f"Vector rebuilt successfully ({pages} pages)",

            "success",

        )

    except Exception:

        traceback.print_exc()

        flash(

            "Vector rebuild failed.",

            "danger",

        )

    return redirect(
        url_for(
            "documents.index"
        )
    )


# ==========================================================
# PDF Viewer
# ==========================================================

@documents_bp.route(
    "/viewer",
    methods=["GET"],
)
@login_required
def viewer():

    filename = Path(

        request.args.get(
            "file",
            "",
        )

    ).name

    page = request.args.get(

        "page",

        1,

        type=int,

    )

    if not filename:

        abort(404)

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
    methods=["GET"],
)
@login_required
def view_pdf():

    filename = Path(

        request.args.get(
            "file",
            "",
        )

    ).name

    if not filename:

        abort(404)

    pdf = UPLOAD_PATH / filename

    if not pdf.exists():

        abort(404)

    return send_file(

        pdf,

        mimetype="application/pdf",

        as_attachment=False,

        download_name=filename,

    )