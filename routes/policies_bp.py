import os
from datetime import datetime

from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from constants import PLAN_HIERARCHY, UPLOAD_FOLDER
from extensions import db
from models.policies import Policies
from models.policy_types import PolicyType
from routes.account_details_bp import update_profile_pic_if_none

policies_bp = Blueprint("policies_bp", __name__)


@policies_bp.get("/policies")
def policies_screen():
    policy_types = [type.to_dict() for type in PolicyType.query.all()]
    return render_template("policies.html", policy_types=policy_types)


@policies_bp.get("/policies/new-policy/<policy_id>")
@login_required
def new_policy_page(policy_id=None):
    policy_types = [type.to_dict() for type in PolicyType.query.all()]
    return render_template(
        "new-policy.html", policy_id=policy_id, policy_types=policy_types
    )


@policies_bp.post("/policies/new-policy-sign-up")
def new_policy_sign_up():
    data = {
        "username": current_user.username,
        "phone_name": request.form.get("phone_name"),
        "policy_name": request.form.get("radio"),
        "phone_case": request.form.get("phone-case"),
        "screen_protector": request.form.get("screen-protector"),
        "waterproof_phone": request.form.get("waterproof-phone"),
        "image_link": None,
    }

    if "image-file" not in request.files:
        raise ValueError("Please upload a valid image")

    img = request.files["image-file"]

    if img.filename == "":
        raise ValueError("Please upload a valid image")

    if img:
        extension = os.path.splitext(f"{img.filename}")[1]
        filename = f"policy-{datetime.today().strftime('%Y-%m-%d')}-{data['username']}{extension}"

        img.save(os.path.join(str(UPLOAD_FOLDER), str(filename)))

        data["image_link"] = os.path.join(str(UPLOAD_FOLDER), str(filename))

        print("Image uploaded successfully")

    new_policy = Policies(**data)

    try:
        db.session.add(new_policy)
        db.session.commit()

        update_profile_pic_if_none(current_user.username, data["image_link"])

        return redirect(url_for("dashboard_bp.dashboard_page"))
    except Exception as e:
        db.session.rollback()  # restores data, cannot be done after commit()
        print(e)
        return redirect(url_for("home_bp.home_screen"))
