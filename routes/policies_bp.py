import os
from datetime import datetime

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from constants import UPLOAD_FOLDER
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
    selected_policy = request.form.get("radio")
    phone_name = request.form.get("phone_name")

    if not selected_policy or not phone_name:
        flash("Please select a policy type and enter phone name", "error")
        return redirect(url_for("policies_bp.new_policy_page"))

    # Get policy type details
    policy_type = PolicyType.query.filter_by(name=selected_policy).first()
    if not policy_type:
        flash("Invalid policy type selected", "error")
        return redirect(url_for("policies_bp.new_policy_page"))

    img_path = request.form.get("image-file")
    img_link = request.form.get("image")

    data = {
        "premium": policy_type.start_price,
        "phone_name": phone_name,
        "policy_name": selected_policy,
        "phone_case": request.form.get("phone-case") == "true",  # Convert to boolean
        "screen_protector": request.form.get("screen-protector") == "true",
        "waterproof_phone": request.form.get("waterproof-phone") == "true",
        "username": current_user.username,
        "policy_type_id": policy_type.policy_type_id,
        "image_link": img_link if img_link else img_path,  # Your existing logic
    }
    print(data)
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


@policies_bp.route("/upgrade/<string:policy_id>")
@login_required
def upgrade_page(policy_id):
    # Get both the policy and its type in one query
    result = (
        db.session.query(Policies, PolicyType)
        .join(PolicyType, Policies.policy_type_id == PolicyType.policy_type_id)
        .filter(
            Policies.policy_id == policy_id, Policies.username == current_user.username
        )
        .first()
    )

    if not result:
        abort(404)

    current_policy, current_policy_type = result

    # Get higher-tier plans
    higher_policy_types_query = (
        PolicyType.query.filter(
            PolicyType.start_price > current_policy_type.start_price
        )
        .order_by(PolicyType.start_price)
        .all()
    )

    # Create a list of tuples with (policy_type, simulated_policy)
    higher_policy_types = []
    for pt in higher_policy_types_query:
        # Create a simulated policy with premium for display purposes
        simulated_policy = type(
            "obj",
            (object,),
            {"premium": pt.start_price, "policy_type_id": pt.policy_type_id},
        )
        higher_policy_types.append((pt, simulated_policy))

    # Get the policy_type object for the current policy
    policy_type = PolicyType.query.get(current_policy.policy_type_id)

    return render_template(
        "upgrade.html",
        current_policy=current_policy,
        current_policy_type=current_policy_type,
        policy_type=policy_type,  # Add this for compatibility
        higher_policy_types=higher_policy_types,
        phone_name=current_policy.phone_name,
    )


@policies_bp.route("/confirm-upgrade", methods=["POST"])
@login_required
def confirm_upgrade():
    policy_id = request.form.get("policy_id")
    new_policy_type_id = request.form.get("new_policy_type_id")

    if not policy_id or not new_policy_type_id:
        flash("Missing required fields", "danger")
        return redirect(url_for("dashboard_bp.dashboard_page"))

    # Verify the policy belongs to the user
    policy = Policies.query.filter_by(
        policy_id=policy_id, username=current_user.username
    ).first()

    if not policy:
        abort(404)

    # Get the new policy type
    new_policy_type = PolicyType.query.filter_by(
        policy_type_id=new_policy_type_id
    ).first()

    if not new_policy_type:
        abort(404)

    # Apply premium discounts based on user selections
    discount = 0
    if request.form.get("phone-case") == "on":
        policy.phone_case = "Yes"
        discount += 0.05
    if request.form.get("screen-protector") == "on":
        policy.screen_protector = "Yes"
        discount += 0.03
    if request.form.get("waterproof-phone") == "on":
        policy.waterproof_phone = "Yes"
        discount += 0.02

    # Update the policy
    policy.policy_name = new_policy_type.name
    policy.policy_type_id = new_policy_type.policy_type_id
    original_premium = new_policy_type.start_price
    policy.premium = original_premium * (1 - discount)

    try:
        db.session.commit()
        flash(f"Successfully upgraded to {new_policy_type.name} Plan!", "success")
    except Exception as e:
        db.session.rollback()
        flash("Failed to process upgrade. Please try again.", "danger")

    return redirect(url_for("dashboard_bp.dashboard_page"))
