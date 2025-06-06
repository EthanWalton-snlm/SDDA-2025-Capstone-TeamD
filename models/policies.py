import uuid

from sqlalchemy import ForeignKey

from extensions import db
from models.policy_types import PolicyType


class Policies(db.Model):
    __tablename__ = "policies"
    policy_id = db.Column(
        db.String(50), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    username = db.Column(db.String(100), ForeignKey("users.username"))

    phone_name = db.Column(db.String(100))
    policy_name = db.Column(db.String(100))
    policy_type_id = db.Column(db.String(50), ForeignKey(PolicyType.policy_type_id))
    phone_case = db.Column(db.Boolean)
    screen_protector = db.Column(db.Boolean)
    waterproof_phone = db.Column(db.Boolean)
    image_link = db.Column(db.String(500), nullable=True)
    premium = db.Column(db.Float)

    # Object -> Dict
    def to_dict(self):
        return {
            "policy_id": self.policy_id,
            "username": self.username,
            "policy_name": self.policy_name,
            "phone_name": self.phone_name,
            "policy_type_id": self.policy_type_id,
            "phone_case": self.phone_case,
            "screen_protector": self.screen_protector,
            "waterproof_phone": self.waterproof_phone,
            "image_link": self.image_link,  # Include the image_link in the dictionary
            "premium": self.premium,
        }

    def get_id(self):
        return self.policy_id
