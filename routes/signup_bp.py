from flask import Blueprint, render_template

signup_bp = Blueprint("signup_bp", __name__)


@signup_bp.get("/sign-up")
def log_in_screen():
    return render_template("signup.html")
