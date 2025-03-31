from flask import Blueprint, render_template

claims_bp = Blueprint("claims_bp", __name__)


@claims_bp.get("/")
def claims_page():
    return render_template("claims.html")
