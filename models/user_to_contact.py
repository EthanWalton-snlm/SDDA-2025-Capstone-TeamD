from extensions import db


class UsersToContact(db.Model):
    __tablename__ = "usersToContact"
    id_number = db.Column(db.String(13), primary_key=True)
    name = db.Column(db.String(50))
    surname = db.Column(db.String(50))
    email = db.Column(db.String(50))
    phone_number = db.Column(db.String(13))
    method_of_contact = db.Column(db.String(50))
    message = db.Column(db.String(500))

    # Object -> Dict
    def to_dict(self):
        return {
            "name": self.name,
            "surnamee": self.surname,
            "email": self.email,
            "phone_number": self.phone_number,
            "method_of_contact": self.method_of_contact,
            "id_number": self.id_number,
            "message": self.message,
        }

    def get_id(self):
        return self.id_number
