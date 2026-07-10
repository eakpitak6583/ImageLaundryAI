from flask import Blueprint
from flask import render_template

from services.customer_dashboard_service import (

    customers,

)

customer = Blueprint(

    "customer",

    __name__,

)


@customer.route("/customers")

def customer_list():

    return render_template(

        "customers.html",

        customers=customers(),

    )