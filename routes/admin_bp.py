from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from constants import CLAIM_STATUS_CODE
from extensions import db
from models.claims import Claim
from models.users import User
from routes import dashboard_bp

admin_bp = Blueprint("admin_bp", __name__)


def get_all_submissions_data():
    submissions_query = Claim.query.all()
    return [submission.to_dict() for submission in submissions_query]


def get_all_approved_submissions():
    submissions = get_all_submissions_data()
    return [
        submission
        for submission in submissions
        if submission["status"] == CLAIM_STATUS_CODE["approve"]
    ]


# TODO: reject goes to approved


def get_all_rejected_submissions():
    submissions = get_all_submissions_data()
    return [
        submission
        for submission in submissions
        if submission["status"] == CLAIM_STATUS_CODE["reject"]
    ]


def get_all_pending_submissions():
    submissions = get_all_submissions_data()
    return [
        submission
        for submission in submissions
        if submission["status"] == CLAIM_STATUS_CODE["pending"]
    ]


# TODO: only allow admin accs
@admin_bp.route("/")
@login_required
def admin_home_page():
    if current_user.is_admin == 1:
        return render_template(
            "admin.html",
            submissions=get_all_submissions_data(),
            approved=get_all_approved_submissions(),
            rejected=get_all_rejected_submissions(),
        )

    return redirect(url_for("dashboard_bp.dashboard_page"))


@admin_bp.route("/review/<id>", methods=["GET", "POST"])
@login_required
def admin_review(id):
    submission = next(
        item for item in get_all_submissions_data() if item["claim_id"] == id
    )

    if request.method == "POST":
        user = User.query.get(submission["username"])

        if not user:
            return redirect(url_for("claims_bp.claims_page"))

        if "approve" in request.form:
            user.claims_approved = user.claims_approved + 1
            user.claims_pending = user.claims_pending - 1
            amount_approved = request.form.get("amount-approved")
            change_claim_status(
                submission["claim_id"], CLAIM_STATUS_CODE["approve"], user
            )
            update_amount_approved(submission["claim_id"], amount_approved)
            return redirect(url_for("admin_bp.admin_home_page"))
        elif "reject" in request.form:
            user.claims_rejected = user.claims_rejected + 1
            user.claims_pending = user.claims_pending - 1
            change_claim_status(
                submission["claim_id"], CLAIM_STATUS_CODE["reject"], user
            )
            return redirect(url_for("admin_bp.admin_review", id=id))
        elif "admin_comment" in request.form:
            update_claim_reason(
                submission["claim_id"], request.form.get("admin_comment")
            )
            return redirect(url_for("admin_bp.admin_home_page"))
        # Redirect back to the home page
        # return redirect(url_for("home_bp.home_screen"))

    return render_template("admin_review.html", submission=submission)


def change_claim_status(id, status, user):
    claim = Claim.query.get(id)
    if claim is not None:
        try:
            claim.status = status
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()  # restores data, cannot be done after commit()
            print(e)


def update_amount_approved(id, amount_approved):
    claim = Claim.query.get(id)

    if claim is not None:
        try:
            claim.amount_approved = amount_approved
            db.session.commit()
        except Exception as e:
            db.session.rollback()  # restores data, cannot be done after commit()
            print(e)


# I will use the below change_claim_status once I've fixed my DB issues

# # Function to change claim status and store the admin username
# def change_claim_status(id, status):
#     claim = Claim.query.get(id)

#     if claim is not None:
#         try:
#             claim.status = status  # Change the claim status

#             # Store the username of the admin who approved or rejected the claim
#             if status == CLAIM_STATUS_CODE["approve"]:
#                 claim.approved_by = (
#                     current_user.username
#                 )  # Save the admin username who approved
#             elif status == CLAIM_STATUS_CODE["reject"]:
#                 claim.rejected_by = (
#                     current_user.username
#                 )  # Save the admin username who rejected

#             db.session.commit()  # Commit the changes to the database
#         except Exception as e:
#             db.session.rollback()  # If an error occurs, rollback the transaction
#             print(e)


def update_claim_reason(id, admin_comment):
    claim = Claim.query.get(id)

    if claim is not None:
        try:
            claim.admin_comment = admin_comment
            db.session.commit()
        except Exception as e:
            db.session.rollback()  # restores data, cannot be done after commit()
            print(e)


# @admin_bp.post("/new-claim")
# def add_claim():
#     data = {
#         "username": request.form.get("username"),
#         "password":  # encrypt_password(
#         request.form.get("password"),
#         # ),  # TODO: encrypt in html [using encrypt_password()]
#         "first_name": request.form.get("first_name"),
#         "last_name": request.form.get("last_name"),
#         "email": request.form.get("email"),
#         "phone_number": request.form.get("phone_number"),
#         "id_number": request.form.get("id_number"),
#     }

#     new_user = Claim(**data)

#     try:
#         db.session.add(new_user)
#         db.session.commit()
#         return redirect(url_for("dashboard_bp.dashboard_page"))
#     except Exception as e:
#         db.session.rollback()  # restores data, cannot be done after commit()
#         print(e)
#         return redirect(url_for("home_bp.home_screen"))
