import uuid

from extensions import db
from models.policy_types import PolicyType
from sqlalchemy import ForeignKey


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
    policy_id = db.Column(db.String(50), ForeignKey(PolicyType.policy_type_id))
    affidavit_link = db.Column(db.String(500), nullable=True)
    image_link = db.Column(db.String(500), nullable=True)

    # Object -> Dict
    def to_dict(self):
        return {
            # "user_id": self.user_id,
            "claim_id": self.claim_id,
            "status": self.status,
            "reason": self.reason,
            "admin_comment": self.admin_comment,
            "username": self.username,
            "policy_id": self.policy_id,
            "affidavit_link": self.affidavit_link,
            "image_link": self.image_link,
        }
