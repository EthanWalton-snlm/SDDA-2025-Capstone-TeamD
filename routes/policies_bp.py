from flask import Blueprint, render_template

policies_bp = Blueprint("policies_bp", __name__)


@policies_bp.get("/policies")
def policies_screen():
    return render_template("policies.html")


@policies_bp.get("/policies/new-policy")
def new_policy_page():
    return render_template("new-policy.html")
