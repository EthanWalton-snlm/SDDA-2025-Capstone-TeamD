from flask import Blueprint, redirect, render_template, request, url_for

admin_bp = Blueprint("admin_bp", __name__)

# Temp - will be in DB (TODO)

submissions = [
    {
        "id": 1,
        "name": "John Doe",
        "submitted": "Form submitted by John Doe",
        "status": "pending",
        "reason": "",
    },
    {
        "id": 2,
        "name": "Jane Smith",
        "submitted": "Form submitted by Jane Smith",
        "status": "pending",
        "reason": "",
    },
    {
        "id": 2,
        "name": "Jane Smith",
        "submitted": "Form submitted by Jane Smith",
        "status": "pending",
        "reason": "",
    },
    {
        "id": 2,
        "name": "Jane Smith",
        "submitted": "Form submitted by Jane Smith",
        "status": "pending",
        "reason": "",
    },
    {
        "id": 2,
        "name": "Jane Smith",
        "submitted": "Form submitted by Jane Smith",
        "status": "pending",
        "reason": "",
    },
    {
        "id": 2,
        "name": "Jane Smith",
        "submitted": "Form submitted by Jane Smith",
        "status": "pending",
        "reason": "",
    },
    {
        "id": 2,
        "name": "Jane Smith",
        "submitted": "Form submitted by Jane Smith",
        "status": "pending",
        "reason": "",
    },
    {
        "id": 2,
        "name": "Jane Smith",
        "submitted": "Form submitted by Jane Smith",
        "status": "pending",
        "reason": "",
    },
    {
        "id": 2,
        "name": "Jane Smith",
        "submitted": "Form submitted by Jane Smith",
        "status": "pending",
        "reason": "",
    },
    {
        "id": 2,
        "name": "Jane Smith",
        "submitted": "Form submitted by Jane Smith",
        "status": "pending",
        "reason": "",
    },
    {
        "id": 2,
        "name": "Jane Smith",
        "submitted": "Form submitted by Jane Smith",
        "status": "pending",
        "reason": "",
    },
    {
        "id": 2,
        "name": "Jane Smith",
        "submitted": "Form submitted by Jane Smith",
        "status": "pending",
        "reason": "",
    },
    {
        "id": 2,
        "name": "Jane Smith",
        "submitted": "Form submitted by Jane Smith",
        "status": "pending",
        "reason": "",
    },
    {
        "id": 2,
        "name": "Jane Smith",
        "submitted": "Form submitted by Jane Smith",
        "status": "pending",
        "reason": "",
    },
    {
        "id": 2,
        "name": "Jane Smith",
        "submitted": "Form submitted by Jane Smith",
        "status": "pending",
        "reason": "",
    },
]

approved = []

rejected = []


@admin_bp.route("/")
def admin_home_page():
    return render_template(
        "admin.html", submissions=submissions, approved=approved, rejected=rejected
    )


@admin_bp.route("/review/<int:id>", methods=["GET", "POST"])
def admin_review(id):
    submission = next(item for item in submissions if item["id"] == id)

    if request.method == "POST":
        if "approve" in request.form:
            submission["status"] = "approved"
            approved.append(submission)
        elif "reject" in request.form:
            submission["status"] = "rejected"
            submission["reason"] = request.form["reason"]
            rejected.append(submission)

        # Redirect back to the home page
        return redirect(url_for("home_bp.home_screen"))

    return render_template("admin_review.html", submission=submission)
