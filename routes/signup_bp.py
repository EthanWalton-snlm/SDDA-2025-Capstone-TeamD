from flask import Blueprint, redirect, render_template, request, url_for

from constants import set_logged_in_username
from extensions import db
from models.users import User
from utilities import encrypt_password

signup_bp = Blueprint("signup_bp", __name__)


@signup_bp.get("/sign-up")
def sign_up_screen():
    return render_template("signup.html")


@signup_bp.post("/new-sign-up")
def sign_up_user():
    data = {
        "username": request.form.get("username"),
        "password": encrypt_password(
            request.form.get("password")
        ),  # TODO: encrypt in html [using encrypt_password()]
        "first_name": request.form.get("first_name"),
        "last_name": request.form.get("last_name"),
        "email": request.form.get("email"),
        "phone_number": request.form.get("phone_number"),
        "id_number": request.form.get("id_number"),
    }

    new_user = User(**data)

    try:
        db.session.add(new_user)
        db.session.commit()
        set_logged_in_username(new_user.to_dict()["username"])
        return redirect(url_for("dashboard_bp.dashboard_page"))
    except Exception as e:
        db.session.rollback()  # restores data, cannot be done after commit()
        print(e)
        return redirect(url_for("home_bp.home_screen"))
