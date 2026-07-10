"""
Image Laundry AI
Machine Master Routes
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

from config import Config

from services.machine_master_service import (
    machine_master_service,
)

from services.file_service import (
    file_service,
)


machine_master_bp = Blueprint(
    "machine_master",
    __name__,
    url_prefix="/machine-master",
)


# ==========================================================
# Machine Master List
# ==========================================================

@machine_master_bp.route("/", methods=["GET"])
@login_required
def index():

    keyword = request.args.get(
        "q",
        "",
    ).strip()

    if keyword:

        machines = machine_master_service.search(
            keyword
        )

    else:

        machines = machine_master_service.get_all()

    return render_template(

        "machine_master.html",

        machines=machines,

        keyword=keyword,

    )


# ==========================================================
# Machine Detail
# ==========================================================

@machine_master_bp.route(
    "/<int:machine_id>",
    methods=["GET"],
)
@login_required
def detail(machine_id):

    machine = machine_master_service.get(
        machine_id
    )

    if not machine:

        flash(
            "Machine not found.",
            "warning",
        )

        return redirect(
            url_for(
                "machine_master.index"
            )
        )

    return render_template(

        "machine_master_detail.html",

        machine=machine,

    )


# ==========================================================
# Create
# ==========================================================

@machine_master_bp.route(
    "/create",
    methods=["POST"],
)
@login_required
def create():

    data = request.form.to_dict()

    image = request.files.get(
        "image_file"
    )

    if image and image.filename:

        data["image_file"] = file_service.save(

            image,

            Config.MACHINE_IMAGE_FOLDER,

        )

    manual = request.files.get(
        "manual_file"
    )

    if manual and manual.filename:

        data["manual_file"] = file_service.save(

            manual,

            Config.MANUAL_UPLOAD_FOLDER,

        )

    result = machine_master_service.create(
        data
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
        url_for(
            "machine_master.index"
        )
    )


# ==========================================================
# Update
# ==========================================================

@machine_master_bp.route(
    "/<int:machine_id>/update",
    methods=["POST"],
)
@login_required
def update(machine_id):

    data = request.form.to_dict()

    image = request.files.get(
        "image_file"
    )

    if image and image.filename:

        data["image_file"] = file_service.save(

            image,

            Config.MACHINE_IMAGE_FOLDER,

        )

    manual = request.files.get(
        "manual_file"
    )

    if manual and manual.filename:

        data["manual_file"] = file_service.save(

            manual,

            Config.MANUAL_UPLOAD_FOLDER,

        )

    result = machine_master_service.update(

        machine_id,

        data,

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

            "machine_master.detail",

            machine_id=machine_id,

        )

    )


# ==========================================================
# Delete
# ==========================================================

@machine_master_bp.route(
    "/<int:machine_id>/delete",
    methods=["POST"],
)
@login_required
def delete(machine_id):

    result = machine_master_service.delete(
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

        url_for(

            "machine_master.index"

        )

    )