from flask import Blueprint, render_template
from flask_login import current_user, login_required

from models.policies import Policies
from models.users import User

dashboard_bp = Blueprint("dashboard_bp", __name__)


@dashboard_bp.get("/")
@login_required
def dashboard_page():
    return render_template(
        "dashboard.html", policies=Policies.query.all(), user=current_user.to_dict()
    )
