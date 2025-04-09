from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from extensions import db

# from models.claims import Claim
from models.policies import Policies
from models.policy_types import PolicyType
from models.users import User

dashboard_bp = Blueprint("dashboard_bp", __name__)


@dashboard_bp.get("/")
@login_required
def dashboard_page():
    if not current_user.is_authenticated:
        return redirect(url_for("auth_bp.login_page"))

    # # Get policies for the current user
    # policies = Policies.query.filter_by(user_id=current_user.id).all()
    # return render_template("dashboard.html", user=current_user, policies=policies)
    return render_template(
        "dashboard.html",
        policies=Policies.query.all(),
        policy_types=PolicyType.query.all(),
        user=current_user.to_dict(),
        stored_users=User.query.all(),
    )
