from flask import Blueprint, render_template
from flask_login import login_required

from constants import get_logged_in_username
from models.users import User

dashboard_bp = Blueprint("dashboard_bp", __name__)


@dashboard_bp.get("/")
@login_required
def dashboard_page():
    print("welcome " + get_logged_in_username())
    # print(get_policies())
    return render_template("dashboard.html")
