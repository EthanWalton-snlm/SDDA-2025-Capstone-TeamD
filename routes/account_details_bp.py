from flask import Blueprint, redirect, render_template, url_for

from constants import get_logged_in_username
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
