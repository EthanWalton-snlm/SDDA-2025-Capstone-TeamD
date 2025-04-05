from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
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


# @auth_bp.post("/login")
# def submit_login_page():
#     username = request.form.get("username")
#     password = request.form.get("password")

#     try:
#         if not username:
#             flash("Username must be filled", "error")
#             return redirect(url_for("auth_bp.login_page"))

#         if not password:
#             flash("Password must be filled", "error")
#             return redirect(url_for("auth_bp.login_page"))

#         user_from_db = User.query.filter_by(username=username).first()

#         if not (user_from_db and check_password_hash(user_from_db.password, password)):
#             flash("Invalid credentials", "error")
#             return redirect(url_for("auth_bp.login_page"))
#         login_user(
#             user_from_db
#         )  # Create token & store in cookies for that particular user

#         if user_from_db.is_admin:
#             flash("Welcome Admin", "success")
#             return redirect(url_for("admin_bp.admin_page"))  # Admin dashboard route
#         else:
#             flash("Welcome User", "success")
#             return redirect(
#                 url_for("dashboard_bp.dashboard_page")
#             )  # User dashboard route

#     except Exception as e:
#         print("ERROR:", e)
#         db.session.rollback()
#         return redirect(url_for("auth_bp.login_page"))


@auth_bp.post("/login")
def submit_login_page():
    username = request.form.get("username")
    password = request.form.get("password")

    try:
        if not username:
            flash("Username must be filled", "error")
            print("No username provided")
            return redirect(url_for("auth_bp.login_page"))

        if not password:
            flash("Password must be filled", "error")
            print("No password provided")
            return redirect(url_for("auth_bp.login_page"))

        user_from_db = User.query.filter_by(username=username).first()

        if not user_from_db:
            flash("Invalid username", "error")
            print("No user found with the provided username")
            return redirect(url_for("auth_bp.login_page"))

        if not check_password_hash(user_from_db.password, password):
            flash("Invalid password", "error")
            print("Invalid password entered")
            return redirect(url_for("auth_bp.login_page"))

        # If we reached here, the login is successful
        login_user(user_from_db)

        if user_from_db.is_admin:
            flash("Welcome Admin", "success")
            return redirect(
                url_for("admin_bp.admin_home_page")
            )  # Redirect to the admin home page
        else:
            flash("Welcome User", "success")
            return redirect(
                url_for("dashboard_bp.dashboard_page")
            )  # Regular user dashboard

    except Exception as e:
        print("ERROR:", e)
        db.session.rollback()
        flash("An error occurred during login. Please try again.", "error")
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
        print(generate_password_hash("admin"))
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

        flash("Sign-up successful! You can now log in.", "success")
        return redirect(url_for("auth_bp.login_page"))

        # return redirect(url_for("dashboard_bp.dashboard_page"))
    except Exception as e:
        print("ERROR:", e)
        db.session.rollback()
        return redirect(url_for("home_bp.home_screen"))


@login_required
@auth_bp.get("/logout")
def logout_page():
    logout_user()
    return redirect(url_for("home_bp.home_screen"))


@auth_bp.post("/contact-us")
def contact_us_page():
    username = request.form.get("name")
    password = request.form.get("surname")

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
        print("ERROR:", e)
        db.session.rollback()
        return redirect(url_for("auth_bp.login_page"))
