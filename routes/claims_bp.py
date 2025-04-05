## dashboard functionality comes before
from flask import Blueprint, render_template, request
from flask_login import current_user, login_required

from extensions import db
from models.claims import Claim
from models.policy_types import PolicyType

claims_bp = Blueprint("claims_bp", __name__)


@claims_bp.get("/")
@login_required
def claims_page():
    policy_types = PolicyType.query.all()
    return render_template("claims.html", policy_types=policy_types)


@claims_bp.post("/submit")
@login_required
def submit_claim():
    # Get form data
    policy_id = request.form.get("policy_id")
    reason = request.form.get("reason")
    affidavit_link = request.form.get("affidavit_link")
    image_link = request.form.get("image_link")
    submission_date = request.form.get("submission_date")
    date_of_incident = request.form.get("date_of_incident")

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
        data = {
            "status": "Pending",
            "reason": reason,
            "admin_comment": "",
            "username": current_user.username,
            "policy_id": policy_id,
            "affidavit_link": affidavit_link,
            "image_link": image_link,
            "submission_date": submission_date,
            "date_of_incident": date_of_incident,
        }
        new_claim = Claim(**data)

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
