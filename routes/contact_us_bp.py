from flask import Blueprint, render_template

contact_us_bp = Blueprint("contact_us_bp", __name__)


@contact_us_bp.get("/contact-us")
def contact_us_screen():
    return render_template("contact-us.html")
