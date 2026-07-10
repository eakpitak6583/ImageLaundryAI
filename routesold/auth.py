from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash

from flask_login import login_user
from flask_login import logout_user

from services.auth_service import authenticate

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "GET":
        return render_template("login.html")

    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    user = authenticate(username, password)

    if user is None:

        flash("Username หรือ Password ไม่ถูกต้อง")

        return redirect(url_for("auth.login"))

    login_user(user)

    return redirect("/dashboard")


@auth.route("/logout")
def logout():

    logout_user()

    return redirect(url_for("auth.login"))