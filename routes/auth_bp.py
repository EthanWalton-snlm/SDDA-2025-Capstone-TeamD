from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from extensions import db
from models.users import User

auth_bp = Blueprint("auth_bp", __name__)


@auth_bp.get("/login")
def login_page():
    return render_template("login.html")


@auth_bp.get("/signup")
def signup_page():
    return render_template("signup.html")


@auth_bp.post("/login")
def submit_login_page():
    username = request.form.get("username")
    password = request.form.get("password")

    try:
        if not username:
            raise ValueError("Username must be filled")

        if not password:
            raise ValueError("Password must be filled")

        user_from_db = User.query.filter_by(username=username).first()

        if not (user_from_db and check_password_hash(user_from_db.password, password)):
            raise ValueError("Credentials not valid")

        login_user(
            user_from_db
        )  # Create token & store in cookies for that particular user

        return redirect(url_for("dashboard_bp.dashboard_page"))
    except Exception as e:
        print(e)
        db.session.rollback()
        return redirect(url_for("auth_bp.login_page"))


@auth_bp.post("/signup")
def submit_signup_page():
    username = request.form.get("username")
    password = request.form.get("password")
    confirm = request.form.get("confirm")

    try:
        if not username:
            raise ValueError("Username must be filled")

        if not password:
            raise ValueError("Password must be filled")

        if password != confirm:
            raise ValueError("Password does not match")

        hashed_password = generate_password_hash(password)

        data = {
            "username": username,
            "password": hashed_password,
            "first_name": request.form.get("first_name"),
            "last_name": request.form.get("last_name"),
            "email": request.form.get("email"),
            "phone_number": request.form.get("phone_number"),
            "id_number": request.form.get("id_number"),
        }

        new_user = User(**data)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("dashboard_bp.dashboard_page"))
    except Exception as e:
        print(e)
        db.session.rollback()
        return redirect(url_for("home_bp.home_screen"))


@auth_bp.get("/logout")
def logout_page():
    logout_user()
    return redirect(url_for("home_bp.home_screen"))
