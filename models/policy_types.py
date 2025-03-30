import uuid

from extensions import db


class PolicyType(db.Model):
    __tablename__ = "policyTypes"

    policy_type_id = db.Column(
        db.String(50), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    name = db.Column(db.String(100))
    summary = db.Column(db.String(500))

    # Object -> Dict
    def to_dict(self):
        return {
            # "user_id": self.user_id,
            "policy_type_id": self.policy_type_id,
            "name": self.name,
            "summary": self.summary,
        }
