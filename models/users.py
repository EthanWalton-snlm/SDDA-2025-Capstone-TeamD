from flask_login import UserMixin

from extensions import db


class User(UserMixin, db.Model):
    __tablename__ = "users"
    # user_id = db.Column(
    #     db.String(50), primary_key=True, default=lambda: str(uuid.uuid4())
    # )
    username = db.Column(db.String(100), primary_key=True)
    password = db.Column(db.String(5000))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    phone_number = db.Column(db.String(13))
    id_number = db.Column(db.String(13))
    profile_pic = db.Column(db.String(500))
    is_admin = db.Column(db.Boolean, default=False)

    claims_made = db.Column(db.Integer, default=0)
    claims_approved = db.Column(db.Integer, default=0)
    claims_rejected = db.Column(db.Integer, default=0)
    claims_pending = db.Column(db.Integer, default=0)

    # Object -> Dict
    def to_dict(self):
        return {
            # "user_id": self.user_id,
            "username": self.username,
            "password": self.password,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone_number": self.phone_number,
            "id_number": self.id_number,
            "profile_pic": self.profile_pic,
            "is_admin": self.is_admin,
            "claims_made": self.claims_made,
            "claims_approved": self.claims_approved,
            "claims_rejected": self.claims_rejected,
            "claims_pending": self.claims_pending,
        }

    def get_id(self):
        return self.username
