"""
LaundryBot V7 Enterprise
Customer Routes
"""

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
)

from flask_login import login_required

from services.customer_service import customer_service


customer_bp = Blueprint(
    "customer",
    __name__,
    url_prefix="/customers",
)


@customer_bp.route("/", methods=["GET"])
@login_required
def index():

    keyword = request.args.get("q", "").strip()

    if keyword:
        customers = customer_service.search(keyword)
    else:
        customers = customer_service.get_all()

    return render_template(
        "customers.html",
        customers=customers,
        keyword=keyword,
    )


@customer_bp.route("/<int:customer_id>", methods=["GET"])
@login_required
def detail(customer_id):

    customer = customer_service.get(customer_id)

    return render_template(
        "customer_detail.html",
        customer=customer,
    )


@customer_bp.route("/create", methods=["POST"])
@login_required
def create():

    customer_service.create(request.form)

    return redirect(
        url_for("customer.index")
    )


@customer_bp.route("/<int:customer_id>/update", methods=["POST"])
@login_required
def update(customer_id):

    customer_service.update(
        customer_id,
        request.form,
    )

    return redirect(
        url_for(
            "customer.detail",
            customer_id=customer_id,
        )
    )


@customer_bp.route("/<int:customer_id>/delete", methods=["POST"])
@login_required
def delete(customer_id):

    customer_service.delete(customer_id)

    return redirect(
        url_for("customer.index")
    )