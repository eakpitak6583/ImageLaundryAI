from flask import Blueprint
from flask import render_template

from services.machine_dashboard_service import *

machine_bp = Blueprint(

    "machine",

    __name__,

)


@machine_bp.route("/machines")

def machine_list():

    return render_template(

        "machines.html",

        machines=machines(),

    )


@machine_bp.route("/machine/<int:machine_id>")

def machine_detail(machine_id):

    return render_template(

        "machine_detail.html",

        machine=machine(machine_id),

    )