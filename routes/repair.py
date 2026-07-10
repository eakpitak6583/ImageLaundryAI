"""
LaundryBot V7 Enterprise
Repair Routes
"""

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
)

from flask_login import login_required

from services.repair_service import repair_service


repair_bp = Blueprint(
    "repair",
    __name__,
    url_prefix="/repairs",
)


@repair_bp.route("/", methods=["GET"])
@login_required
def index():

    keyword = request.args.get("q", "").strip()

    if keyword:
        repairs = repair_service.search(keyword)
    else:
        repairs = repair_service.get_all()

    return render_template(
        "repair.html",
        repairs=repairs,
        keyword=keyword,
    )


@repair_bp.route("/<int:repair_id>", methods=["GET"])
@login_required
def detail(repair_id):

    repair = repair_service.get(repair_id)

    return render_template(
        "repair_detail.html",
        repair=repair,
    )


@repair_bp.route("/create", methods=["POST"])
@login_required
def create():

    repair_service.create(request.form)

    return redirect(
        url_for("repair.index")
    )


@repair_bp.route("/<int:repair_id>/update", methods=["POST"])
@login_required
def update(repair_id):

    repair_service.update(
        repair_id,
        request.form,
    )

    return redirect(
        url_for(
            "repair.detail",
            repair_id=repair_id,
        )
    )


@repair_bp.route("/<int:repair_id>/delete", methods=["POST"])
@login_required
def delete(repair_id):

    repair_service.delete(repair_id)

    return redirect(
        url_for("repair.index")
    )