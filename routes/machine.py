"""
LaundryBot V7 Enterprise
Machine Routes
"""

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
)

from flask_login import login_required

from services.machine_service import machine_service


machine_bp = Blueprint(
    "machine",
    __name__,
    url_prefix="/machines",
)


@machine_bp.route("/")
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


@machine_bp.route("/<int:machine_id>")
@login_required
def detail(machine_id):

    machine = machine_service.get(machine_id)

    return render_template(
        "machine_detail.html",
        machine=machine,
    )


@machine_bp.route("/create", methods=["POST"])
@login_required
def create():

    machine_service.create(request.form)

    return redirect(url_for("machine.index"))


@machine_bp.route("/<int:machine_id>/update", methods=["POST"])
@login_required
def update(machine_id):

    machine_service.update(
        machine_id,
        request.form,
    )

    return redirect(
        url_for(
            "machine.detail",
            machine_id=machine_id,
        )
    )


@machine_bp.route("/<int:machine_id>/delete", methods=["POST"])
@login_required
def delete(machine_id):

    machine_service.delete(machine_id)

    return redirect(
        url_for("machine.index")
    )