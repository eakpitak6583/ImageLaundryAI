"""
Image Laundry AI
Authentication Routes
"""

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
)

from flask_login import (
    login_user,
    logout_user,
    login_required,
)

from services.auth_service import auth_service
from models.user import User


auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth",
)


# ==========================================================
# Login
# ==========================================================

@auth_bp.route(
    "/login",
    methods=["GET", "POST"],
)
def login():

    if request.method == "POST":

        username = request.form.get(
            "username",
            "",
        ).strip()

        password = request.form.get(
            "password",
            "",
        )

        user = auth_service.login(

            username,

            password,

        )

        if user:

            login_user(

                User(user),

                remember=True,

            )

            next_url = request.args.get("next")

            if next_url:

                return redirect(next_url)

            return redirect(

                url_for("dashboard.index")

            )

        flash(

            "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง",

            "danger",

        )

    return render_template(
        "login.html"
    )


# ==========================================================
# Logout
# ==========================================================

@auth_bp.route("/logout")
@login_required
def logout():

    logout_user()

    flash(

        "ออกจากระบบเรียบร้อยแล้ว",

        "success",

    )

    return redirect(

        url_for("auth.login")

    )