from flask import Blueprint, redirect, url_for

from constants import set_logged_in_username

signout_bp = Blueprint("signout_bp", __name__)


@signout_bp.get("/")
def sign_out_user():
    set_logged_in_username("")

    return redirect(url_for("home_bp.home_screen"))
