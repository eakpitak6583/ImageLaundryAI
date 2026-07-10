"""
Image Laundry AI
Customer Routes
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

from services.customer_service import customer_service


customer_bp = Blueprint(
    "customer",
    __name__,
    url_prefix="/customers",
)


# ==========================================================
# Customer List
# ==========================================================

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


# ==========================================================
# Customer Detail
# ==========================================================

@customer_bp.route("/<int:customer_id>", methods=["GET"])
@login_required
def detail(customer_id):

    customer = customer_service.get(customer_id)

    if not customer:

        flash(
            "Customer not found.",
            "warning",
        )

        return redirect(
            url_for("customer.index")
        )

    return render_template(
        "customer_detail.html",
        customer=customer,
    )


# ==========================================================
# Create Customer
# ==========================================================

@customer_bp.route("/create", methods=["POST"])
@login_required
def create():

    result = customer_service.create(
        request.form
    )

    if result.get("success"):

        flash(
            "Customer created successfully.",
            "success",
        )

    else:

        flash(
            result.get(
                "message",
                "Unable to create customer.",
            ),
            "danger",
        )

    return redirect(
        url_for("customer.index")
    )


# ==========================================================
# Update Customer
# ==========================================================

@customer_bp.route(
    "/<int:customer_id>/update",
    methods=["POST"],
)
@login_required
def update(customer_id):

    result = customer_service.update(
        customer_id,
        request.form,
    )

    if result.get("success"):

        flash(
            "Customer updated successfully.",
            "success",
        )

    else:

        flash(
            result.get(
                "message",
                "Unable to update customer.",
            ),
            "danger",
        )

    return redirect(
        url_for(
            "customer.detail",
            customer_id=customer_id,
        )
    )


# ==========================================================
# Delete Customer
# ==========================================================

@customer_bp.route(
    "/<int:customer_id>/delete",
    methods=["POST"],
)
@login_required
def delete(customer_id):

    result = customer_service.delete(
        customer_id
    )

    if result.get("success"):

        flash(
            "Customer deleted successfully.",
            "success",
        )

    else:

        flash(
            result.get(
                "message",
                "Unable to delete customer.",
            ),
            "danger",
        )

    return redirect(
        url_for("customer.index")
    )