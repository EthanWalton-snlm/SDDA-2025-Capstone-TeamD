from functools import wraps

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from extensions import db
from models import claims
from models.claims import Claim
from models.policy_types import PolicyType

claims_bp = Blueprint("claims_bp", __name__)


# # Function to check if user is logged in
# def login_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if "username" not in session:
#             # flash("Please log in to access this page", "error")
#             return redirect(url_for("login_bp.login"))
#         return f(*args, **kwargs)

#     return decorated_function


@claims_bp.get("/")
# @login_required
def claims_page():
    policy_types = PolicyType.query.all()
    return render_template("claims.html", policy_types=policy_types)


@claims_bp.post("/submit")
# @login_required
def submit_claim():
    # Get form data
    policy_id = request.form.get("policy_id")
    reason = request.form.get("reason")

    # Basic form validation
    if not policy_id or not reason:
        return render_template(
            "claims.html",
            error="All fields are required",
            policy_types=PolicyType.query.all(),
        )

    if len(reason) > 500:
        return render_template(
            "claims.html",
            error="Reason must be less than 500 characters",
            policy_types=PolicyType.query.all(),
        )

    # Create new claim
    try:
        new_claim = Claim(
            status="Pending",  # Initial status
            reason=reason,
            admin_comment="",  # Empty initially
            username=session.get("username"),  # Get username from session
            policy_id=policy_id,
        )

        # Add and commit to database
        db.session.add(new_claim)
        db.session.commit()

        # Return success
        return render_template(
            "claims.html",
            success="Your claim has been submitted successfully. Claim ID: "
            + new_claim.claim_id,
            policy_types=PolicyType.query.all(),
        )

    except Exception as e:
        db.session.rollback()
        return render_template(
            "claims.html",
            error=f"An error occurred: {str(e)}",
            policy_types=PolicyType.query.all(),
        )
