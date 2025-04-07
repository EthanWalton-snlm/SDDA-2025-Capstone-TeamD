from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user

from extensions import db
from models.users import User

account_details_bp = Blueprint("account_details_bp", __name__)


def update_profile_pic_if_none(username, link):
    user = get_user_details(username)

    if user is not None:
        data = user.to_dict()

        if data["profile_pic"] is None:
            return update_profile_pic(username, link)

    return False


def update_profile_pic(username, link):
    user = get_user_details(username)

    if user is not None:
        new_data = {"profile_pic": link}

        updated_data = user.to_dict() | new_data

        try:
            User.query.filter_by(username=username).update(updated_data)

            db.session.commit()
        except Exception:
            db.session.rollback()
            return False

        return True

    return False


def get_user_details(username):
    return User.query.get(username)


@account_details_bp.get("/")
def account_details_page():
    user = current_user.to_dict()
    profile_pic_url = "https://th.bing.com/th/id/OIP.V8o0z-WF2LgCV-e2c0MSRAHaHa?w=1306&h=1306&rs=1&pid=ImgDetMain"

    if user["profile_pic"] is not None:
        profile_pic_url = user["profile_pic"]

    return render_template(
        "account-details.html",
        user=user,
        edit=False,
        profile_pic_url=profile_pic_url,
    )


@account_details_bp.get("/edit")
def edit_account_details_page():
    user = current_user.to_dict()
    profile_pic_url = "https://th.bing.com/th/id/OIP.V8o0z-WF2LgCV-e2c0MSRAHaHa?w=1306&h=1306&rs=1&pid=ImgDetMain"

    if user["profile_pic"] is not None:
        profile_pic_url = user["profile_pic"]

    return render_template(
        "account-details.html",
        user=current_user.to_dict(),
        edit=True,
        profile_pic_url=profile_pic_url,
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
