"""
LaundryBot V5

Machine Route
"""

import os

from flask import (
    Blueprint,
    render_template,
    request,
    send_from_directory,
    abort,
)

from flask_login import login_required

from services.machine_service import (
    get_all_machines,
    get_machine,
)

machine = Blueprint(
    "machine",
    __name__,
)

# ==========================================================
# Manual Folder
# ==========================================================

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

MANUAL_FOLDER = os.path.join(
    BASE_DIR,
    "manuals",
    "pdf",
)


# ==========================================================
# Machine List
# ==========================================================

@machine.route("/machines")
@login_required
def machine_list():

    keyword = request.args.get("q", "").strip()

    machines = get_all_machines(keyword)

    return render_template(
        "machine.html",
        machines=machines,
        keyword=keyword,
    )


# ==========================================================
# Machine Detail
# ==========================================================

@machine.route("/machines/<model>")
@login_required
def machine_detail(model):

    machine_data = get_machine(model)

    if machine_data is None:

        return "Machine Not Found", 404

    return render_template(
        "machine_detail.html",
        machine=machine_data,
    )


# ==========================================================
# Open PDF Manual
# ==========================================================

@machine.route("/manual/<path:filename>")
@login_required
def open_manual(filename):

    filepath = os.path.join(
        MANUAL_FOLDER,
        filename,
    )

    if not os.path.exists(filepath):

        abort(404)

    return send_from_directory(
        MANUAL_FOLDER,
        filename,
    )