import uuid

from sqlalchemy import ForeignKey

from extensions import db
from models.policies import Policies
from models.policy_types import PolicyType


class Claim(db.Model):
    __tablename__ = "claims"
    claim_id = db.Column(
        db.String(50), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    status = db.Column(db.String(25))
    reason = db.Column(db.String(500))
    admin_comment = db.Column(db.String(500))
    username = db.Column(
        db.String(100), ForeignKey("users.username")
    )  # aka submitted_by
    # policy_id = db.Column(db.String(50), ForeignKey(PolicyType.policy_type_id))
    policy_id = db.Column(db.String(50), ForeignKey(Policies.policy_id))
    affidavit_link = db.Column(db.String(500), nullable=True)
    image_link = db.Column(db.String(500), nullable=True)

    quotation_link = db.Column(db.String(500), nullable=True)
    submission_date = db.Column(db.DateTime, nullable=False, default=db.func.now())
    date_of_incident = db.Column(db.Date, nullable=False)

    # New fields to store admin info
    approved_by = db.Column(db.String(100), nullable=True)
    rejected_by = db.Column(db.String(100), nullable=True)

    claim_amount = db.Column(db.Float)
    amount_approved = db.Column(db.Float)

    # Object -> Dict
    def to_dict(self):
        return {
            "claim_id": self.claim_id,
            "status": self.status,
            "reason": self.reason,
            "admin_comment": self.admin_comment,
            "username": self.username,
            "policy_id": self.policy_id,
            "affidavit_link": self.affidavit_link,
            "image_link": self.image_link,
            "quotation_link": self.quotation_link,
            "approved_by": self.approved_by,
            "rejected_by": self.rejected_by,
            "submission_date": self.submission_date,
            "date_of_incident": self.date_of_incident,
            "claim_amount": self.claim_amount,
            "amount_approved": self.amount_approved,
        }
