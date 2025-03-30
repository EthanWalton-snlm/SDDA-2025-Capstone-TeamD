from flask import Blueprint, redirect, render_template, request, url_for

from constants import set_logged_in_username
from routes.account_details_bp import get_user_details
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

    user = get_user_details(data["username"])

    if user is None:
        return redirect(url_for("login_bp.log_in_screen"))

    print(user.to_dict()["password"], data["password"])

    if encrypt_password(user.to_dict()["password"]) == data["password"]:
        set_logged_in_username(user.to_dict()["username"])
        return redirect(url_for("dashboard_bp.dashboard_page"))
    else:
        return redirect(url_for("login_bp.log_in_screen"))
