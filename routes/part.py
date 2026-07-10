"""
LaundryBot V7 Enterprise
Part Routes
"""

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
)

from flask_login import login_required

from services.part_service import part_service


part_bp = Blueprint(
    "part",
    __name__,
    url_prefix="/parts",
)


@part_bp.route("/")
@login_required
def index():

    keyword = request.args.get("q", "").strip()

    if keyword:
        parts = part_service.search(keyword)
    else:
        parts = part_service.get_all()

    return render_template(
        "part.html",
        parts=parts,
        keyword=keyword,
    )


@part_bp.route("/<int:part_id>")
@login_required
def detail(part_id):

    part = part_service.get(part_id)

    return render_template(
        "part_detail.html",
        part=part,
    )


@part_bp.route("/create", methods=["POST"])
@login_required
def create():

    part_service.create(request.form)

    return redirect(url_for("part.index"))


@part_bp.route("/<int:part_id>/update", methods=["POST"])
@login_required
def update(part_id):

    part_service.update(
        part_id,
        request.form,
    )

    return redirect(
        url_for(
            "part.detail",
            part_id=part_id,
        )
    )


@part_bp.route("/<int:part_id>/delete", methods=["POST"])
@login_required
def delete(part_id):

    part_service.delete(part_id)

    return redirect(url_for("part.index"))