from flask import Blueprint, render_template

from models.users import User

account_details_bp = Blueprint("account_details_bp", __name__)


def get_user_details(username):
    return User.query.get(username)


@account_details_bp.get("/")
def account_details_page():
    return render_template("account-details.html")
