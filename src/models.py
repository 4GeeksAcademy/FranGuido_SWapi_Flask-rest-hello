from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorite = db.relationship('Favorite', back_populates='user')

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
    """ favorite = db.relationship('Favorite', back_populates='planet') """

    # Print planet info
    def __repr__(self):
        return f"Planet {self.name} with ID {self.id}"

    def serialize(self):
        return {
            "id" : self.id,
            "name" : self.name
        }
    
# Star Wars Characters table
class Characters(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    """ favorite = db.relationship('Favorite', back_populates='character') """


    #Print characters info
    def __repr__(self):
        return f"Character {self.name} with ID {self.id}"
    
    def serialize(self):
        return {
            "id" : self.id,
            "name": self.name
        }
    
# Favorites table
class Favorite(db.Model):
    __tablename__ = 'favorite'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='favorite')
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', back_populates='favorite')
    # The FK of Planets and Characters
    category_fk_id = db.Column(db.Integer)

    # Print Favorite info
    def __repr__(self):
        return f"Favorite {self.name} with ID {self.id}"
    
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "category_id": self.category_id,
            "category_fk_id": self.category_fk_id
        }
    
# Category of Favorite (Planet or Character) table
class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(30))
    favorite = db.relationship('Favorite', back_populates='category')

    # Print Category info
    def __repr__(self):
        return f"Category {self.category_name}"
    
    def serialize(self):
        return {
            "id": self.id,
            "category_name": self.category_name
        }

