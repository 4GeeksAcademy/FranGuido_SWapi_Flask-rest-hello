from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return f"User with email {self.email} and id {self.id}" # Shows msg with the user email and id

    def serialize(self): # how info will be returned as dictionaries
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }