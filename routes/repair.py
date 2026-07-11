"""
LaundryBot V7 Enterprise
Repair Routes
"""

import logging
import os

from flask import (

    Blueprint,

    current_app,

    flash,

    redirect,

    render_template,

    request,

    url_for,

)

from flask_login import (

    login_required,

)

from werkzeug.utils import (

    secure_filename,

)

from services.repair_service import (

    repair_service,

)


repair_bp = Blueprint(

    "repair",

    __name__,

    url_prefix="/repairs",

)


logger = logging.getLogger(

    __name__,

)


# ==========================================================
# Allowed File
# ==========================================================

def allowed_file(

    filename,

):

    if not filename:

        return False

    return (

        "." in filename

        and

        filename.rsplit(

            ".",

            1,

        )[1].lower() == "pdf"

    )


# ==========================================================
# Validate Upload
# ==========================================================

def validate_upload(

    file,

):

    if file is None:

        return False, "No file uploaded."

    if file.filename == "":

        return False, "Please select PDF file."

    if not allowed_file(

        file.filename,

    ):

        return False, "Only PDF files are allowed."

    return True, ""


# ==========================================================
# Repair List
# ==========================================================
@repair_bp.route(

    "/",

    methods=[

        "GET",

    ],

)

@login_required
def index():

    keyword = request.args.get(

        "q",

        "",

    ).strip()

    logger.info(

        "Repair Search : %s",

        keyword,

    )

    if keyword:

        repairs = repair_service.search(

            keyword,

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

    methods=[

        "GET",

    ],

)

@login_required
def detail(

    repair_id,

):

    repair = repair_service.get(

        repair_id,

    )

    if repair is None:

        flash(

            "Repair record not found.",

            "warning",

        )

        return redirect(

            url_for(

                "repair.index",

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

    methods=[

        "POST",

    ],

)

@login_required
def create():

    data = request.form.to_dict()

    result = repair_service.create(

        data,

    )

    if result.get(

        "success",

    ):

        flash(

            "Repair created successfully.",

            "success",

        )

        return redirect(

            url_for(

                "repair.detail",

                repair_id=result["repair_id"],

            )

        )

    flash(

        result.get(

            "message",

            "Unable to create repair.",

        ),

        "danger",

    )

    return redirect(

        url_for(

            "repair.index",

        )

    )


# ==========================================================
# Update
# ==========================================================

@repair_bp.route(

    "/<int:repair_id>/update",

    methods=[

        "POST",

    ],

)

@login_required
def update(

    repair_id,

):

    repair = repair_service.get(

        repair_id,

    )

    if repair is None:

        flash(

            "Repair record not found.",

            "warning",

        )

        return redirect(

            url_for(

                "repair.index",

            )

        )

    result = repair_service.update(

        repair_id,

        request.form.to_dict(),

    )

    if result.get(

        "success",

    ):

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

    methods=[

        "POST",

    ],

)

@login_required
def delete(

    repair_id,

):

    repair = repair_service.get(

        repair_id,

    )

    if repair is None:

        flash(

            "Repair record not found.",

            "warning",

        )

        return redirect(

            url_for(

                "repair.index",

            )

        )

    result = repair_service.delete(

        repair_id,

    )

    if result.get(

        "success",

    ):

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

            "repair.index",

        )

    )


# ==========================================================
# AI Import
# ==========================================================

@repair_bp.route(

    "/import",

    methods=[

        "GET",

        "POST",

    ],

)

@login_required
def import_pdf():

    if request.method == "GET":

        return render_template(

            "repair_import.html",

        )

    file = request.files.get(

        "file",

    )

    valid, message = validate_upload(

        file,

    )

    if not valid:

        flash(

            message,

            "warning",

        )

        return redirect(

            url_for(

                "repair.import_pdf",

            )

        )

    filename = secure_filename(

        file.filename,

    )

    upload_folder = os.path.join(

        current_app.config.get(

            "UPLOAD_FOLDER",

            "uploads",

        ),

        "repair",

    )

    os.makedirs(

        upload_folder,

        exist_ok=True,

    )

    filepath = os.path.join(

        upload_folder,

        filename,

    )

    file.save(

        filepath,

    )

    try:

        result = repair_service.import_pdf(

            filepath,

        )

    except Exception as e:

        logger.exception(

            e,

        )

        flash(

            str(e),

            "danger",

        )

        return redirect(

            url_for(

                "repair.import_pdf",

            )

        )

    return render_template(

        "repair_preview.html",

        repair=result["data"],

    )


# ==========================================================
# Preview
# ==========================================================

@repair_bp.route(

    "/preview",

    methods=[

        "POST",

    ],

)

@login_required
def preview():

    data = request.form.to_dict()

    return render_template(

        "repair_preview.html",

        repair=data,

    )


# ==========================================================
# Confirm Import
# ==========================================================
@repair_bp.route(

    "/confirm-import",

    methods=[

        "POST",

    ],

)

@login_required
def confirm_import():

    data = request.form.to_dict()

    logger.info(

        "Confirm AI Import"

    )

    try:

        result = repair_service.create(

            data,

        )

    except Exception as e:

        logger.exception(

            e,

        )

        flash(

            str(e),

            "danger",

        )

        return redirect(

            url_for(

                "repair.import_pdf",

            )

        )

    if not result.get(

        "success",

    ):

        flash(

            result.get(

                "message",

                "Unable to create repair.",

            ),

            "warning",

        )

        return redirect(

            url_for(

                "repair.import_pdf",

            )

        )

    flash(

        "Repair imported successfully.",

        "success",

    )

    return redirect(

        url_for(

            "repair.detail",

            repair_id=result[

                "repair_id"

            ],

        )

    )


# ==========================================================
# Re Import
# ==========================================================

@repair_bp.route(

    "/<int:repair_id>/reimport",

    methods=[

        "POST",

    ],

)

@login_required
def reimport(

    repair_id,

):

    repair = repair_service.get(

        repair_id,

    )

    if repair is None:

        flash(

            "Repair record not found.",

            "warning",

        )

        return redirect(

            url_for(

                "repair.index",

            )

        )

    filepath = repair.get(

        "report_file",

        "",

    )

    if filepath == "":

        flash(

            "Original PDF not found.",

            "warning",

        )

        return redirect(

            url_for(

                "repair.detail",

                repair_id=repair_id,

            )

        )

    try:

        result = repair_service.import_pdf(

            filepath,

        )

    except Exception as e:

        logger.exception(

            e,

        )

        flash(

            str(e),

            "danger",

        )

        return redirect(

            url_for(

                "repair.detail",

                repair_id=repair_id,

            )

        )

    return render_template(

        "repair_preview.html",

        repair=result["data"],

    )


# ==========================================================
# Latest Repairs
# ==========================================================
@repair_bp.route(

    "/latest",

    methods=[

        "GET",

    ],

)

@login_required
def latest():

    repairs = repair_service.latest(

        limit=20,

    )

    return render_template(

        "repair_latest.html",

        repairs=repairs,

    )


# ==========================================================
# Repair Status
# ==========================================================

@repair_bp.route(

    "/<int:repair_id>/status",

    methods=[

        "GET",

    ],

)

@login_required
def status(

    repair_id,

):

    repair = repair_service.get(

        repair_id,

    )

    if repair is None:

        flash(

            "Repair record not found.",

            "warning",

        )

        return redirect(

            url_for(

                "repair.index",

            )

        )

    return render_template(

        "repair_status.html",

        repair=repair,

    )


# ==========================================================
# Error Handler
# ==========================================================

@repair_bp.errorhandler(

    404,

)

def not_found(

    error,

):

    flash(

        "Repair page not found.",

        "warning",

    )

    return redirect(

        url_for(

            "repair.index",

        )

    )


@repair_bp.errorhandler(

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

            "repair.index",

        )

    )