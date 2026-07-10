"""
Image Laundry AI
Machine Routes
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

from services.machine_service import machine_service


machine_bp = Blueprint(
    "machine",
    __name__,
    url_prefix="/machines",
)


# ==========================================================
# Machine List
# ==========================================================

@machine_bp.route("/", methods=["GET"])
@login_required
def index():

    keyword = request.args.get("q", "").strip()

    if keyword:
        machines = machine_service.search(keyword)
    else:
        machines = machine_service.get_all()

    return render_template(
        "machine.html",
        machines=machines,
        keyword=keyword,
    )


# ==========================================================
# Machine Detail
# ==========================================================

@machine_bp.route("/<int:machine_id>", methods=["GET"])
@login_required
def detail(machine_id):

    machine = machine_service.get(machine_id)

    if not machine:

        flash(
            "Machine not found.",
            "warning",
        )

        return redirect(
            url_for("machine.index")
        )

    return render_template(
        "machine_detail.html",
        machine=machine,
    )


# ==========================================================
# Create Machine
# ==========================================================

@machine_bp.route("/create", methods=["POST"])
@login_required
def create():

    result = machine_service.create(
        request.form
    )

    if result.get("success"):

        flash(
            "Machine created successfully.",
            "success",
        )

    else:

        flash(
            result.get(
                "message",
                "Unable to create machine.",
            ),
            "danger",
        )

    return redirect(
        url_for("machine.index")
    )


# ==========================================================
# Update Machine
# ==========================================================

@machine_bp.route(
    "/<int:machine_id>/update",
    methods=["POST"],
)
@login_required
def update(machine_id):

    result = machine_service.update(
        machine_id,
        request.form,
    )

    if result.get("success"):

        flash(
            "Machine updated successfully.",
            "success",
        )

    else:

        flash(
            result.get(
                "message",
                "Unable to update machine.",
            ),
            "danger",
        )

    return redirect(
        url_for(
            "machine.detail",
            machine_id=machine_id,
        )
    )


# ==========================================================
# Delete Machine
# ==========================================================

@machine_bp.route(
    "/<int:machine_id>/delete",
    methods=["POST"],
)
@login_required
def delete(machine_id):

    result = machine_service.delete(
        machine_id
    )

    if result.get("success"):

        flash(
            "Machine deleted successfully.",
            "success",
        )

    else:

        flash(
            result.get(
                "message",
                "Unable to delete machine.",
            ),
            "danger",
        )

    return redirect(
        url_for("machine.index")
    )