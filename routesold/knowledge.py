from flask import Blueprint
from flask import render_template

from flask_login import login_required

from services.knowledge_service import get_knowledge_summary
from flask import redirect
from flask import flash

from services.knowledge_service import run_import

knowledge = Blueprint(
    "knowledge",
    __name__,
)


@knowledge.route("/knowledge")
@login_required
def index():

    data = get_knowledge_summary()

    return render_template(
        "knowledge.html",
        data=data,
    )
@knowledge.route("/knowledge/import")
@login_required
def run():

    result = run_import()

    flash(
        f"Imported {len(result)} files."
    )

    return redirect("/knowledge")
    logs = get_import_logs()