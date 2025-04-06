import os
from datetime import datetime

from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from constants import UPLOAD_FOLDER
from extensions import db
from models.policies import Policies

policies_bp = Blueprint("policies_bp", __name__)


@policies_bp.get("/policies")
def policies_screen():
    return render_template("policies.html")


@policies_bp.get("/policies/new-policy/<policy_name>")
@login_required
def new_policy_page(policy_name=None):
    return render_template("new-policy.html", policy_name=policy_name)


@policies_bp.post("/policies/new-policy-sign-up")
def new_policy_sign_up():
    data = {
        "username": current_user.username,
        "phone_name": request.form.get("phone_name"),
        "policy_name": request.form.get("radio"),
        "phone_case": request.form.get("phone-case"),
        "screen_protector": request.form.get("screen-protector"),
        "waterproof_phone": request.form.get("waterproof-phone"),
        "image_link": request.form.get("image"),  # Store the image URL here
    }

    # Validate that image URL is provided (no file upload needed)
    image_link = data.get("image_link")
    if not image_link:
        raise ValueError("Please provide a valid image URL")

    # Make sure the URL is valid (you can add more URL validation as needed)
    if not image_link.startswith("http"):
        raise ValueError("Please provide a valid URL that starts with http or https")

    # Create a new policy record
    new_policy = Policies(**data)

    try:
        db.session.add(new_policy)
        db.session.commit()
        return redirect(url_for("dashboard_bp.dashboard_page"))
    except Exception as e:
        db.session.rollback()  # restores data, cannot be done after commit()
        print(e)
        return redirect(url_for("home_bp.home_screen"))
