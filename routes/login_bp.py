from flask import Blueprint, redirect, render_template, request, url_for

from models.users import User
from utilities import encrypt_password

login_bp = Blueprint("login_bp", __name__)


@login_bp.get("/log-in")
def log_in_screen():
    return render_template("login.html")


@login_bp.post("/log-in-auth")  # TODO: send details in JSON body
def log_in_auth():
    data = {
        "username": request.form.get("username"),
        "password": encrypt_password(
            request.form.get("password")
        ),  # TODO: encrypt in html [using encrypt_password()]
    }

    user = User.query.get(data["username"])

    if user is None:
        return redirect(url_for("login_bp.log_in_screen"))

    user_details = user.to_dict()

    if user_details["password"] == data["password"]:
        return redirect(url_for("dashboard_bp.dashboard_page"))
    else:
        return redirect(url_for("login_bp.log_in_screen"))
