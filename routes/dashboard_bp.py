from flask import Blueprint, render_template
from flask_login import login_required

from models.users import User

dashboard_bp = Blueprint("dashboard_bp", __name__)


@dashboard_bp.get("/")
@login_required
def dashboard_page():
    print("welcome ")
    # print(get_policies())
    return render_template("dashboard.html")
