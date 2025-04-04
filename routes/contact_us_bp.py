from flask import Blueprint, redirect, render_template, request, url_for

from extensions import db
from models.user_to_contact import UsersToContact

contact_us_bp = Blueprint("contact_us_bp", __name__)


@contact_us_bp.get("/contact-us")
def contact_us_screen():
    return render_template("contact-us.html")


@contact_us_bp.post("/contact-us")
def submit_contact_info():
    id_number = request.form.get("id_number")
    name = request.form.get("name")
    surname = request.form.get("surname")
    email = request.form.get("email")
    phone_number = request.form.get("phone_number")
    method_of_contact = request.form.get("method_of_contact")
    message = request.form.get("message")

    try:
        if not name:
            raise ValueError("Name must be filled")
        if not id_number:
            raise ValueError("ID number must be filled")
        if not email:
            raise ValueError("Email must be filled")
        if not phone_number:
            raise ValueError("Phone number must be filled")
        if not method_of_contact:
            raise ValueError("Specify preferred method of contact")
        data = {
            "id_number": id_number,
            "name": name,
            "surname": surname,
            "email": email,
            "phone_number": phone_number,
            "method_of_contact": method_of_contact,
            "message": message,
        }
        print(data)
        user_info = UsersToContact(**data)
        db.session.add(user_info)
        db.session.commit()

        return redirect(url_for("home_bp.home_screen"))
    except Exception as e:
        print("ERROR:", e)
        db.session.rollback()
        return redirect(url_for("contact_us_bp.submit_contact_info"))
