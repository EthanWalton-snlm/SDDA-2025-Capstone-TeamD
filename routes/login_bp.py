from flask import Blueprint, redirect, render_template, url_for

login_bp = Blueprint("login_bp", __name__)


@login_bp.get("/log-in")
def log_in_screen():
    return render_template("login.html")


@login_bp.post("/log-in-auth")  # TODO: send details in JSON body
def log_in_auth():
    return redirect(url_for("dashboard_bp.dashboard_page"))
