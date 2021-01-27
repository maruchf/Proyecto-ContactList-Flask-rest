from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Contact(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(200),  unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.String(250), nullable=False)
    phone = db.Column(db.String(14), unique=False, nullable=False)

    def __repr__(self):
        return '<Contact %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "full_name": self.full_name,
            "address": self.address,
            "phone": self.phone
            # do not serialize the password, its a security breach
        }