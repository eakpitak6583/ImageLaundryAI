from flask import Blueprint, render_template
from flask_login import login_required

from services.service_dashboard_service import get_dashboard


service_dashboard = Blueprint(
    "service_dashboard",
    __name__,
)


@service_dashboard.route("/service-dashboard")
@login_required
def dashboard():

    dashboard = get_dashboard()

    return render_template(

        "service_dashboard.html",

        summary=dashboard["summary"],

        top_complaints=dashboard["top_complaints"],

        top_machines=dashboard["top_machines"],

        top_repairs=dashboard["top_repairs"],

        recent_repairs=dashboard["recent_repairs"],

    )