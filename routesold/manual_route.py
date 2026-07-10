from flask import Blueprint
from flask import render_template

from services.manual_service import (

    manuals,

    manual,

)

manual_bp = Blueprint(

    "manual",

    __name__,

)


@manual_bp.route("/manuals")
def manual_list():

    return render_template(

        "manuals.html",

        manuals=manuals(),

    )


@manual_bp.route("/manual/<filename>")
def view_manual(filename):

    return render_template(

        "manual_view.html",

        manual=manual(filename),

    )