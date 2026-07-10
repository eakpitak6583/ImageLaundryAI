"""
Image Laundry AI
Repair Routes
"""

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
)

from flask_login import login_required

from services.repair_service import repair_service


repair_bp = Blueprint(
    "repair",
    __name__,
    url_prefix="/repairs",
)


# ==========================================================
# Repair List
# ==========================================================

@repair_bp.route("/", methods=["GET"])
@login_required
def index():

    keyword = request.args.get(
        "q",
        "",
    ).strip()

    if keyword:

        repairs = repair_service.search(
            keyword
        )

    else:

        repairs = repair_service.get_all()

    return render_template(

        "repair.html",

        repairs=repairs,

        keyword=keyword,

    )


# ==========================================================
# Repair Detail
# ==========================================================

@repair_bp.route(
    "/<int:repair_id>",
    methods=["GET"],
)
@login_required
def detail(repair_id):

    repair = repair_service.get(
        repair_id
    )

    if not repair:

        flash(
            "Repair record not found.",
            "warning",
        )

        return redirect(
            url_for(
                "repair.index"
            )
        )

    return render_template(

        "repair_detail.html",

        repair=repair,

    )


# ==========================================================
# Create
# ==========================================================

@repair_bp.route(
    "/create",
    methods=["POST"],
)
@login_required
def create():

    result = repair_service.create(
        request.form
    )

    if result.get("success"):

        flash(
            "Repair created successfully.",
            "success",
        )

    else:

        flash(
            result.get(
                "message",
                "Unable to create repair.",
            ),
            "danger",
        )

    return redirect(
        url_for(
            "repair.index"
        )
    )


# ==========================================================
# Update
# ==========================================================

@repair_bp.route(
    "/<int:repair_id>/update",
    methods=["POST"],
)
@login_required
def update(repair_id):

    result = repair_service.update(

        repair_id,

        request.form,

    )

    if result.get("success"):

        flash(
            "Repair updated successfully.",
            "success",
        )

    else:

        flash(
            result.get(
                "message",
                "Unable to update repair.",
            ),
            "danger",
        )

    return redirect(

        url_for(

            "repair.detail",

            repair_id=repair_id,

        )

    )


# ==========================================================
# Delete
# ==========================================================

@repair_bp.route(
    "/<int:repair_id>/delete",
    methods=["POST"],
)
@login_required
def delete(repair_id):

    result = repair_service.delete(
        repair_id
    )

    if result.get("success"):

        flash(
            "Repair deleted successfully.",
            "success",
        )

    else:

        flash(
            result.get(
                "message",
                "Unable to delete repair.",
            ),
            "danger",
        )

    return redirect(

        url_for(

            "repair.index"

        )

    )