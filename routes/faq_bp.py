from flask import Blueprint, render_template

faq_bp = Blueprint("faq_bp", __name__)


@faq_bp.get("/faq")
def faq_screen():
    return render_template("faq.html")
