from flask import Blueprint, render_template, request
from flask_login import login_required

from services.part_service import (
    get_all_parts,
    get_part,
    search_part,
)

part = Blueprint(
    "part",
    __name__,
)


@part.route("/parts")
@login_required
def parts():

    keyword = request.args.get("q", "").strip()

    if keyword:

        rows = search_part(keyword)

    else:

        rows = get_all_parts()

    return render_template(
        "part.html",
        parts=rows,
        keyword=keyword,
    )


@part.route("/parts/<int:part_id>")
@login_required
def part_detail(part_id):

    row = get_part(part_id)

    return render_template(
        "part_detail.html",
        part=row,
    )