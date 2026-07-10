"""
LaundryBot V7 Enterprise
Dashboard Routes
"""

from flask import Blueprint, render_template
from flask_login import login_required

from services.dashboard_service import DashboardService

dashboard_bp = Blueprint(
    "dashboard",
    __name__,
    url_prefix="/dashboard"
)

dashboard_service = DashboardService()


@dashboard_bp.route("/")
@login_required
def index():

    data = dashboard_service.summary()

    return render_template(
        "dashboard.html",
        data=data
    )


@dashboard_bp.route("/summary")
@login_required
def summary():

    return dashboard_service.summary()