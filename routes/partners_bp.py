from flask import Blueprint, render_template

partners_bp = Blueprint("partners_bp", __name__)


@partners_bp.get("/partners")
def partners_screen():
    return render_template("partners.html")
