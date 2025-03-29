from flask import Blueprint, render_template

dashboard_bp = Blueprint("dashboard_bp", __name__)


@dashboard_bp.get("/")
def dashboard_page():
    return render_template("dashboard.html")
