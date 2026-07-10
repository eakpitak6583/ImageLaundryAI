from flask import Blueprint
from flask import render_template

from flask_login import login_required

from services.manual_service import get_manuals

manual = Blueprint(
    "manual",
    __name__,
)


@manual.route("/manuals")
@login_required
def manuals():

    rows = get_manuals()

    return render_template(
        "manual.html",
        manuals=rows,
    )