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


# @policies_bp.route("/upgrade/<string:policy_id>", methods=["GET"])
# @login_required
# def upgrade_policy(policy_id):
#     # Debugging
#     print(f"\n--- Accessing upgrade for policy {policy_id} ---")

#     # 1. Get current policy with ownership check
#     current_policy = Policies.query.filter_by(
#         policy_id=policy_id,
#         user_id=current_user.id,  # Ensure user owns this policy
#     ).first()

#     if not current_policy:
#         flash("Policy not found or you don't have permission", "error")
#         return redirect(url_for("dashboard_bp.dashboard_page"))

#     # 2. Handle missing policy type (set default if needed)
#     if not current_policy.policy_type_id:
#         current_policy.policy_type_id = "FPlane"  # Default to Fresher Plan
#         db.session.commit()
#         flash("Assigned default policy type", "info")

#     # 3. Get current policy type
#     current_policy_type = PolicyType.query.get(current_policy.policy_type_id)
#     if not current_policy_type:
#         flash("Invalid policy type configuration", "error")
#         return redirect(url_for("dashboard_bp.dashboard_page"))

#     # 4. Get higher tier plans
#     higher_plans = (
#         db.session.query(PolicyType, Policies)
#         .join(Policies, PolicyType.policy_type_id == Policies.policy_type_id)
#         .filter(
#             PolicyType.policy_type_id.in_(
#                 [
#                     k
#                     for k, v in PLAN_HIERARCHY.items()
#                     if v > PLAN_HIERARCHY.get(current_policy_type.policy_type_id, 0)
#                 ]
#             )
#         )
#         .all()
#     )

#     return render_template(
#         "upgrade.html",
#         current_policy=current_policy,
#         current_policy_type=current_policy_type,
#         higher_policy_types=higher_plans,
#         phone_name=current_policy.phone_name,
#         plan_hierarchy=PLAN_HIERARCHY,
#     )


# @policies_bp.route("/confirm-upgrade", methods=["POST"])
# @login_required
# def confirm_upgrade():
#     try:
#         # Verify required fields
#         if not all(k in request.form for k in ["policy_id", "new_policy_type_id"]):
#             flash("Missing required information", "error")
#             return redirect(request.referrer or url_for("dashboard_bp.dashboard_page"))

#         policy_id = request.form["policy_id"]
#         new_policy_type_id = request.form["new_policy_type_id"]

#         # Verify policy ownership
#         current_policy = Policies.query.filter_by(
#             policy_id=policy_id, user_id=current_user.id
#         ).first()

#         if not current_policy:
#             flash("Policy not found", "error")
#             return redirect(url_for("dashboard_bp.dashboard_page"))

#         # Validate tier upgrade
#         current_tier = PLAN_HIERARCHY.get(current_policy.policy_type_id, 0)
#         new_tier = PLAN_HIERARCHY.get(new_policy_type_id, 0)

#         if new_tier <= current_tier:
#             flash("You must select a higher tier plan", "error")
#             return redirect(url_for("policies_bp.upgrade_policy", policy_id=policy_id))

#         # Apply premium reducers
#         discount = 0.0
#         if "phone-case" in request.form:
#             discount += 0.05
#         if "screen-protector" in request.form:
#             discount += 0.03
#         if "waterproof-phone" in request.form:
#             discount += 0.02

#         # Update policy
#         current_policy.policy_type_id = new_policy_type_id
#         if current_policy.premium is not None and discount > 0:
#             current_policy.premium *= 1 - discount

#         db.session.commit()
#         flash(f"Successfully upgraded to {new_policy_type_id} plan!", "success")
#         return redirect(url_for("dashboard_bp.dashboard_page"))

#     except Exception as e:
#         db.session.rollback()
#         flash(f"Upgrade failed: {str(e)}", "error")
#         return redirect(request.referrer or url_for("dashboard_bp.dashboard_page"))


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
