from flask import Blueprint
from flask import render_template

from flask_login import login_required
from flask_login import current_user

from services.dashboard_service import get_dashboard_summary

dashboard = Blueprint(
    "dashboard",
    __name__,
)


@dashboard.route("/dashboard")
@login_required
def index():

    summary = get_dashboard_summary()

    return render_template(
        "dashboard.html",
        machines=summary["machines"],
        manuals=summary["manuals"],
        parts=summary["parts"],
        repairs=summary["repairs"],
        user=current_user,
    )