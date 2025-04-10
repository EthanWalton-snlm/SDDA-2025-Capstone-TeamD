## dashboard functionality comes before
from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from extensions import db
from models.claims import Claim

# from models.policy_types import PolicyType
from models.policies import Policies
from models.users import User

claims_bp = Blueprint("claims_bp", __name__)


@claims_bp.get("/")
@login_required
def claims_page():
    # policy_types = PolicyType.query.all()
    policy = Policies.query.all()
    return render_template(
        "claims.html",
        policy=policy,
        user=current_user.to_dict(),
    )  # policy_types=policy_types)


@claims_bp.post("/submit")
@login_required
def submit_claim():
    # Get form data
    policy_id = request.form.get("policy_id")

    reason = request.form.get("reason")
    affidavit_link = request.form.get("affidavit_link")
    image_link = request.form.get("image_link")
    date_of_incident = request.form.get("date_of_incident")
    claim_amount = request.form.get("claim_amount")

    # Basic form validation
    if not policy_id or not reason:
        return render_template(
            "claims.html",
            error="All fields are required",
            policy=Policies.query.all(),
            user=current_user.to_dict(),
            # policy_types=PolicyType.query.all(),
        )

    if len(reason) > 500:
        return render_template(
            "claims.html",
            error="Reason must be less than 500 characters",
            policy=Policies.query.all(),
            user=current_user.to_dict(),
            # policy_types=PolicyType.query.all(),
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
            "date_of_incident": date_of_incident,
            "claim_amount": claim_amount,
        }
        new_claim = Claim(**data)

        # update claim count
        user = User.query.filter_by(username=current_user.username).first()

        if not user:
            return redirect(url_for("claims_bp.claims_page"))

        user.claims_made = user.claims_made + 1
        user.claims_pending = user.claims_pending + 1

        # Add and commit to database
        db.session.add(new_claim)
        db.session.commit()

        return redirect(url_for("dashboard_bp.dashboard_page"))

        # Return success (TODO: fix)
        # return render_template(
        #     "claims.html",
        #     success="Your claim has been submitted successfully. Claim ID: "
        #     + new_claim.claim_id,
        #     # policy_types=PolicyType.query.all(),
        #     policy=Policies.query.all(),
        #     user=current_user.to_dict(),
        # )

    except Exception as e:
        db.session.rollback()
        return render_template(
            "claims.html",
            error=f"An error occurred: {str(e)}",
            policy=Policies.query.all(),
            user=current_user.to_dict(),
            # policy_types=PolicyType.query.all(),
        )


@claims_bp.route("/track")
@login_required
def track_claims():
    # Fetch the user's claims
    user_claims = (
        Claim.query.filter_by(username=current_user.username)
        .order_by(Claim.submission_date.desc())
        .all()
    )
    return render_template("track_claims.html", user_claims=user_claims)
