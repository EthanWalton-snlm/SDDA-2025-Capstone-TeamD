from flask import Blueprint, redirect, render_template, request, url_for

from constants import get_logged_in_username
from extensions import db
from models.users import User

account_details_bp = Blueprint("account_details_bp", __name__)


def get_user_details(username):
    return User.query.get(username)


@account_details_bp.get("/")
def account_details_page():
    details = get_user_details(get_logged_in_username())

    if details is not None:
        return render_template(
            "account-details.html", user=details.to_dict(), edit=False
        )

    return redirect(url_for("login_bp.log_in_screen"))


@account_details_bp.get("/edit")
def edit_account_details_page():
    details = get_user_details(get_logged_in_username())

    if details is not None:
        return render_template(
            "account-details.html", user=details.to_dict(), edit=True
        )

    return redirect(url_for("login_bp.log_in_screen"))


@account_details_bp.post("/edit")
def edit_account_details():
    existing_data = get_user_details(get_logged_in_username())

    if existing_data is not None:
        existing_data = existing_data.to_dict()

        changed_data = {
            "first_name": request.form.get("first_name"),
            "last_name": request.form.get("last_name"),
            "email": request.form.get("email"),
            "phone_number": request.form.get("phone_number"),
        }

        updated_data = existing_data | changed_data

        try:
            User.query.filter_by(username=get_logged_in_username()).update(updated_data)

            db.session.commit()
        except Exception:
            db.session.rollback()

    return redirect(url_for("account_details_bp.account_details_page"))

    # details = get_user_details(get_logged_in_username())

    # if details is not None:
    #     return render_template(
    #         "account-details.html", user=details.to_dict(), edit=True
    #     )

    # return redirect(url_for("login_bp.log_in_screen"))
