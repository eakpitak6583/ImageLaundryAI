from flask import (
    Blueprint,
    render_template,
    request,
)
from flask_login import login_required

from services.service_report_service import (
    search_everything,
)

service_report = Blueprint(
    "service_report",
    __name__,
)


@service_report.route(
    "/service-report",
    methods=["GET", "POST"],
)
@login_required
def service_report_page():

    keyword = ""

    rows = []

    if request.method == "POST":

        keyword = request.form.get(
            "keyword",
            "",
        ).strip()

        rows = search_everything(
            keyword,
        )

    return render_template(

        "service_report.html",

        keyword=keyword,

        repairs=rows,

    )