from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user

from extensions import db
from models.policies import Policies
from models.users import User

account_details_bp = Blueprint("account_details_bp", __name__)


def get_user_details(username, policy_id):
    return User.query.get(username)


@account_details_bp.get("/")
def account_details_page():
    return render_template(
        "account-details.html", user=current_user.to_dict(), edit=False
    )


@account_details_bp.get("/edit")
def edit_account_details_page():
    return render_template(
        "account-details.html", user=current_user.to_dict(), edit=True
    )


@account_details_bp.post("/edit")
def edit_account_details():
    changed_data = {
        "first_name": request.form.get("first_name"),
        "last_name": request.form.get("last_name"),
        "email": request.form.get("email"),
        "phone_number": request.form.get("phone_number"),
    }

    updated_data = current_user.to_dict() | changed_data

    try:
        User.query.filter_by(username=current_user.username).update(updated_data)

        db.session.commit()
    except Exception:
        db.session.rollback()

    return redirect(url_for("account_details_bp.account_details_page"))
