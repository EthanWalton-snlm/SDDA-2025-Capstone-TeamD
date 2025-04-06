import os
from datetime import datetime
from email.policy import Policy

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from constants import PLAN_HIERARCHY, UPLOAD_FOLDER
from extensions import db
from models.policies import Policies
from models.policy_types import PolicyType

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
    img_path = request.form.get("image-file")
    img_link = request.form.get("image")

    data = {
        "username": current_user.username,
        "phone_name": request.form.get("phone_name"),
        "policy_name": request.form.get("radio"),
        "phone_case": request.form.get("phone-case"),
        "screen_protector": request.form.get("screen-protector"),
        "waterproof_phone": request.form.get("waterproof-phone"),
        "image_link": img_link if img_link is not None else img_path,
    }

    if "image" not in request.files:
        # Validate that image URL is provided (no file upload needed)
        image_link = data.get("image_link")
        if not image_link:
            raise ValueError("Please provide a valid image URL")

        # Make sure the URL is valid (you can add more URL validation as needed)
        if not image_link.startswith("http"):
            raise ValueError(
                "Please provide a valid URL that starts with http or https"
            )
    else:
        img = request.files["image"]

        if img.filename == "":
            raise ValueError("Please upload a valid image")

        if img:
            filename = f"{data['username']}-policy-{datetime.date}"

            img.save(os.path.join(str(UPLOAD_FOLDER), str(filename)))

            data["image_link"] = os.path.join(str(UPLOAD_FOLDER), str(filename))

            print("Image uploaded successfully")

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
