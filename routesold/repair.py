from flask import Blueprint, render_template
from flask_login import login_required

from services.repair_service import (
    get_all_repairs,
    get_repair,
)

repair = Blueprint(
    "repair",
    __name__,
)


@repair.route("/repairs")
@login_required
def repairs():

    rows = get_all_repairs()

    return render_template(
        "repair.html",
        repairs=rows,
    )


@repair.route("/repairs/<int:repair_id>")
@login_required
def repair_detail(repair_id):

    row = get_repair(repair_id)

    return render_template(
        "repair_detail.html",
        repair=row,
    )