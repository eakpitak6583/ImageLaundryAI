"""
LaundryBot V7 Enterprise
Manual Routes
"""

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
)

from flask_login import login_required

from services.manual_service import manual_service


manual_bp = Blueprint(
    "manual",
    __name__,
    url_prefix="/manuals",
)


@manual_bp.route("/")
@login_required
def index():

    keyword = request.args.get("q", "").strip()

    if keyword:
        manuals = manual_service.search(keyword)
    else:
        manuals = manual_service.get_all()

    return render_template(
        "manual.html",
        manuals=manuals,
        keyword=keyword,
    )


@manual_bp.route("/<int:manual_id>")
@login_required
def detail(manual_id):

    manual = manual_service.get(manual_id)

    return render_template(
        "manual_view.html",
        manual=manual,
    )


@manual_bp.route("/create", methods=["POST"])
@login_required
def create():

    manual_service.create(request.form)

    return redirect(url_for("manual.index"))


@manual_bp.route("/<int:manual_id>/update", methods=["POST"])
@login_required
def update(manual_id):

    manual_service.update(
        manual_id,
        request.form,
    )

    return redirect(
        url_for(
            "manual.detail",
            manual_id=manual_id,
        )
    )


@manual_bp.route("/<int:manual_id>/delete", methods=["POST"])
@login_required
def delete(manual_id):

    manual_service.delete(manual_id)

    return redirect(url_for("manual.index"))