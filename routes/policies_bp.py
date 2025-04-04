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


@policies_bp.get("/policies/new-policy")
@login_required
def new_policy_page():
    return render_template("new-policy.html")


@policies_bp.post("/policies/new-policy-sign-up")
def new_policy_sign_up():
    data = {
        "username": current_user.username,
        "phone_name": request.form.get("phone_name"),
        "policy_name": request.form.get("radio"),
        "phone_case": request.form.get("phone-case"),
        "screen_protector": request.form.get("screen-protector"),
        "waterproof_phone": request.form.get("waterproof-phone"),
    }

    if "image" not in request.files:
        raise ValueError("Please upload a valid image")

    img = request.files["image"]

    if img.filename == "":
        raise ValueError("Please upload a valid image")

    if img:
        extension = os.path.splitext(f"{img.filename}")[1]
        filename = f"policy-{datetime.today().strftime('%Y-%m-%d')}-{data['username']}{extension}"

        img.save(os.path.join(str(UPLOAD_FOLDER), str(filename)))

        print("Image uploaded successfully")

    new_policy = Policies(**data)
    # print(new_user.to_dict())
    try:
        db.session.add(new_policy)
        db.session.commit()
        return redirect(url_for("dashboard_bp.dashboard_page"))
    except Exception as e:
        db.session.rollback()  # restores data, cannot be done after commit()
        print(e)
        return redirect(url_for("home_bp.home_screen"))
