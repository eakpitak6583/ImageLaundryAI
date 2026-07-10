"""
LaundryBot V7 Enterprise
Technician Routes
"""

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
)

from flask_login import login_required

from services.technician_service import technician_service


technician_bp = Blueprint(
    "technician",
    __name__,
    url_prefix="/technicians",
)


@technician_bp.route("/", methods=["GET"])
@login_required
def index():

    keyword = request.args.get("q", "").strip()

    if keyword:
        technicians = technician_service.search(keyword)
    else:
        technicians = technician_service.get_all()

    return render_template(
        "technicians.html",
        technicians=technicians,
        keyword=keyword,
    )


@technician_bp.route("/<int:technician_id>", methods=["GET"])
@login_required
def detail(technician_id):

    technician = technician_service.get(technician_id)

    return render_template(
        "technician_detail.html",
        technician=technician,
    )


@technician_bp.route("/create", methods=["POST"])
@login_required
def create():

    technician_service.create(request.form)

    return redirect(
        url_for("technician.index")
    )


@technician_bp.route("/<int:technician_id>/update", methods=["POST"])
@login_required
def update(technician_id):

    technician_service.update(
        technician_id,
        request.form,
    )

    return redirect(
        url_for(
            "technician.detail",
            technician_id=technician_id,
        )
    )


@technician_bp.route("/<int:technician_id>/delete", methods=["POST"])
@login_required
def delete(technician_id):

    technician_service.delete(technician_id)

    return redirect(
        url_for("technician.index")
    )