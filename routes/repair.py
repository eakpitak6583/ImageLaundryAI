"""
LaundryBot V7 Enterprise
Repair Routes
"""

import os

from flask import (

    Blueprint,

    render_template,

    request,

    redirect,

    url_for,

    flash,

    current_app,

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
# ==========================================================
# AI Import Page
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

    # ------------------------------------------------------
    # Upload File
    # ------------------------------------------------------

    if "file" not in request.files:

        flash(

            "Please select PDF file.",

            "warning",

        )

        return redirect(

            url_for(

                "repair.import_pdf",

            )

        )

    file = request.files["file"]

    if file.filename == "":

        flash(

            "Please select PDF file.",

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

    # ------------------------------------------------------
    # AI Import
    # ------------------------------------------------------

    try:

        result = repair_service.import_pdf(

            filepath,

        )

    except Exception as e:

        flash(

            str(e),

            "danger",

        )

        return redirect(

            url_for(

                "repair.import_pdf",

            )

        )

    flash(

        "AI Import completed successfully.",

        "success",

    )

    return redirect(

        url_for(

            "repair.detail",

            repair_id=result["repair_id"],

        )

    )


# ==========================================================
# Create
# ==========================================================
# ==========================================================
# AI Preview
# ==========================================================

@repair_bp.route(

    "/preview/<int:repair_id>",

    methods=[

        "GET",

    ],

)

@login_required
def preview(

    repair_id,

):

    repair = repair_service.get(

        repair_id,

    )

    if not repair:

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

        "repair_preview.html",

        repair=repair,

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

    try:

        result = repair_service.create(

            data,

        )

        if not result.get(

            "success",

        ):

            flash(

                result.get(

                    "message",

                    "Unable to save repair.",

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

                repair_id=result["repair_id"],

            )

        )

    except Exception as e:

        flash(

            str(e),

            "danger",

        )

        logger.exception(

            e,

        )

        return redirect(

            url_for(

                "repair.import_pdf",

            )

        )

# ==========================================================
# Create
# ==========================================================
# ==========================================================
# Re Import PDF
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

    if not repair:

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

            "danger",

        )

        return redirect(

            url_for(

                "repair.detail",

                repair_id=repair_id,

            )

        )

    try:

        repair_service.import_pdf(

            filepath,

        )

    except Exception as e:

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

    flash(

        "AI Re-import completed.",

        "success",

    )

    return redirect(

        url_for(

            "repair.detail",

            repair_id=repair_id,

        )

    )


# ==========================================================
# Create
# ==========================================================
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
# AI Import Status
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

    if not repair:

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
# Create
# ==========================================================
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
# Before Upload Validation
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
# Error Handler
# ==========================================================

@repair_bp.errorhandler(

    Exception,

)

def handle_exception(

   