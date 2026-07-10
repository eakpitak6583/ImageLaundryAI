"""
LaundryBot V7 Enterprise
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


auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth",
)


# ==========================================================
# Login
# ==========================================================

@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "GET":
        return render_template("login.html")

    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    if username == "" or password == "":

        flash("Please enter username and password.")

        return render_template("login.html")

    user = auth_service.login(
        username,
        password
    )

    if user is None:

        flash("Invalid username or password.")

        return render_template("login.html")

    login_user(user)

    return redirect(
        url_for("dashboard.index")
    )


# ==========================================================
# Logout
# ==========================================================

@auth_bp.route("/logout")
@login_required
def logout():

    logout_user()

    flash("Logged out successfully.")

    return redirect(
        url_for("auth.login")
    )