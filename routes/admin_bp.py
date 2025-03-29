from flask import Blueprint, redirect, render_template, request, url_for

from constants import CLAIM_STATUS_CODE
from extensions import db
from models.claims import Claim

admin_bp = Blueprint("admin_bp", __name__)

# submissions = [
#     {
#         "id": 1,
#         "name": "John Doe",
#         "submitted": "Form submitted by John Doe",
#         "status": "pending",
#         "reason": "",
#     },
#     {
#         "id": 2,
#         "name": "Jane Smith",
#         "submitted": "Form submitted by Jane Smith",
#         "status": "pending",
#         "reason": "",
#     },
#     {
#         "id": 3,
#         "name": "Siyanda Kunene",
#         "submitted": "Form submitted by Siyanda Kunene",
#         "status": "pending",
#         "reason": "",
#     },
#     {
#         "id": 4,
#         "name": "Ethan Walton",
#         "submitted": "Form submitted by Ethan Walton",
#         "status": "pending",
#         "reason": "",
#     },
#     {
#         "id": 5,
#         "name": "Chleo Smith",
#         "submitted": "Form submitted by Chleo Smith",
#         "status": "pending",
#         "reason": "",
#     },
# ]

# approved = []

# rejected = []


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


@admin_bp.route("/")
def admin_home_page():
    return render_template(
        "admin.html",
        submissions=get_all_submissions_data(),
        approved=get_all_approved_submissions(),
        rejected=get_all_rejected_submissions(),
    )


@admin_bp.route("/review/<id>", methods=["GET", "POST"])
def admin_review(id):
    submission = next(
        item for item in get_all_submissions_data() if item["claim_id"] == id
    )

    if request.method == "POST":
        if "approve" in request.form:
            change_claim_status(submission["claim_id"], CLAIM_STATUS_CODE["approve"])
            return redirect(url_for("admin_bp.admin_home_page"))
        elif "reject" in request.form:
            change_claim_status(submission["claim_id"], CLAIM_STATUS_CODE["reject"])
        elif "reject_reason" in request.form:
            change_claim_status(submission["claim_id"], request.form.get("reason"))
            return redirect(url_for("admin_bp.admin_home_page"))
        # Redirect back to the home page
        # return redirect(url_for("home_bp.home_screen"))

    return render_template("admin_review.html", submission=submission)


def change_claim_status(id, status):
    claim = Claim.query.get(id)

    if claim is not None:
        try:
            claim.status = status
            db.session.commit()
        except Exception as e:
            db.session.rollback()  # restores data, cannot be done after commit()
            print(e)


def update_claim_reason(id, reason):
    claim = Claim.query.get(id)

    if claim is not None:
        try:
            claim.reason = reason
            db.session.commit()
        except Exception as e:
            db.session.rollback()  # restores data, cannot be done after commit()
            print(e)


# @admin_bp.post("/new-claim")
# def add_claim():
#     data = {
#         "username": request.form.get("username"),
#         "password": encrypt_password(
#             request.form.get("password")
#         ),  # TODO: encrypt in html [using encrypt_password()]
#         "first_name": request.form.get("first_name"),
#         "last_name": request.form.get("last_name"),
#         "email": request.form.get("email"),
#         "phone_number": request.form.get("phone_number"),
#         "id_number": request.form.get("id_number"),
#     }

#     new_user = User(**data)

#     try:
#         db.session.add(new_user)
#         db.session.commit()
#         return redirect(url_for("dashboard_bp.dashboard_page"))
#     except Exception as e:
#         db.session.rollback()  # restores data, cannot be done after commit()
#         print(e)
#         return redirect(url_for("home_bp.home_screen"))
