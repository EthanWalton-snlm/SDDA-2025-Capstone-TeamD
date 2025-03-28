from flask import Blueprint, render_template

login_bp = Blueprint("login_bp", __name__)


@login_bp.get("/log-in")
def log_in_screen():
    return render_template("login.html")
