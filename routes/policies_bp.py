from flask import Blueprint, redirect, render_template, request, url_for

from extensions import db
from models.policies import Policies

policies_bp = Blueprint("policies_bp", __name__)


@policies_bp.get("/policies")
def policies_screen():
    return render_template("policies.html")


@policies_bp.get("/policies/new-policy")
def new_policy_page():
    return render_template("new-policy.html")


@policies_bp.post("/policies/new-policy-sign-up")
def new_policy_sign_up():
    data = {
        "username": request.form.get("username"),
        "phone_name": request.form.get("phone_name"),
        "policy_name": request.form.get("radio"),
        "phone_case": request.form.get("phone-case"),
        "screen_protector": request.form.get("screen-protector"),
        "waterproof_phone": request.form.get("waterproof-phone"),
    }
    new_user = Policies(**data)
    # print(new_user.to_dict())
    try:
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("dashboard_bp.dashboard_page"))
    except Exception as e:
        db.session.rollback()  # restores data, cannot be done after commit()
        print(e)
        return redirect(url_for("home_bp.home_screen"))
