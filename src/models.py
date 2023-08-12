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
    
 # StarWars Planets table   
class Planets(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)

    # Print planet info
    def __repr__(self):
        return f"Planet {self.name} with ID {self.id}"

    def serialize(self):
        return {
            "id" : self.id,
            "name" : self.name
        }