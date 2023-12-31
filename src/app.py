"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planets, Characters, Favorite, Category
import json

#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# GET ALL USERS
@app.route('/user', methods=['GET'])
def get_users():
    filter_users = User.query.filter_by(is_active = True)
    # print(type(filter_users))
    # print(filter_users)
    filter_users_serialized = list(map(lambda x : x.serialize(), filter_users))
    return jsonify({"msg": 'Completed', "all users": filter_users_serialized})


# GET USER BY ID
@app.route('/user/<int:user_id>', methods=['GET'])
def handle_hello(user_id):
    # Getting all users
    users = User.query.all() #Retrieve all users
    single_user = User.query.get(user_id) # Retrieve single user
    # Return single-user to front-end
    if single_user is None:
        #return jsonify({"msg": f"User with ID {user_id} not found."}), 400
        #APIException also returns msg and bad request code
        raise APIException(f"User with ID {user_id} not found.", status_code=400) 

    #print(single_user)
    users_serialized = list(map(lambda x: x.serialize(), users))
    #print(users_serialized)
    #print(users)
    # Pass user id as parameter and show it in message
    response_body = {
        "msg": "Hello, this is your GET /user response ",
        "users": users_serialized,
        "user_id": user_id,
        "user_info": single_user.serialize() #serialize user info as json format
    }

    return jsonify(response_body), 200

# ADDING NEW USERS WITH POST MEHTOD
@app.route('/user', methods=['POST'])
def post_user():
    body = request.get_json(silent = True)
    if body is None:
        raise APIException("Must give user's information (in body)", status_code=400)
    if "email" not in body:
        raise APIException("Email address is rquired", status_code=400)
    if "password" not in body:
        raise APIException("Must set a password", status_code=400)
    new_user = User(email = body['email'], password = body['password'], is_active = True)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "Completed", "new_user_info": new_user.serialize()})

# USER'S FAVORITES
@app.route('/user/<int:user_id>/favorites', methods=['GET', 'POST', 'DELETE'])
def handle_favorites(user_id = None):
    if user_id is None:
        return jsonify({"msg" : "An User ID is required"}), 400 # Bad request
    
    # GET FAVORITES BY USER ID
    if request.method == 'GET':
        favorites = Favorite.query.filter_by(id=user_id).all()
        return jsonify([x.serialize() for x in favorites]), 200
    
    # ADD FAVORITE WITH METHOD POST
    if request.method == 'POST':
        body = json.loads(request.data)
        category_id = Category.query.filter_by(
            category_name=body['category_name']).first()

        if category_id is None:
            return jsonify({"msg": f"{body['category_name']} is not a valid category"}), 400

        favorite = Favorite(
            user_id=user_id,
            category_id=category_id.id,
            category_fk_id=body['category_fk_id']
        )

        db.session.add(favorite)
        db.session.commit()

        return jsonify({
            "msg": f"Favorite added",
            "inserted_id": f"{favorite.id}"
        }), 200
    
    # DELETING FAVORITE
    if request.method == 'DELETE':
        body = json.loads(request.data)

        category = Category.query.filter_by(
            category_name=body['category_name']).first()

        if category is None:
            return jsonify({"msg": f"{body['category_name']} is not a category"}), 400

        db.session.delete(category)
        db.session.commit()

        return jsonify({
            "msg": f"Category deleted",
            "deleted_id": f"{category.id}"
        }), 200

    return jsonify({"msg": f"{request.method}: Request not valid"}), 400



# GET ALL PLANETS
@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planets.query.all()
    planets_serialized = list(map(lambda x: x.serialize(),planets))
    return jsonify({"msg": 'Completed', "planets": planets_serialized})

# GET SINGLE PLANET
@app.route('/planets/<int:planets_id>', methods=['GET'])
def get_single_planet(planets_id):
    single_planet = Planets.query.get(planets_id)
    response_body = {
        "planets_id" : planets_id,
        "planets_info": single_planet.serialize()
    }
    
    return jsonify(response_body)
    
# ADDING NEW PLANETS WITH METHOD PUT
@app.route('/planets', methods=['PUT'])
def modify_planet():
    body = request.get_json(silent = True)
    if body is None:
        raise APIException("Planet info is required", status_code=400)
    if "id" not in body:
        raise APIException("An ID must be given", status_code=400)
    if "name" not in body:
        raise APIException("A name must be given", status_code=400)
    single_planet = Planets.query.get(body['id'])
    single_planet.name = body['name']
    db.session.commit()
    return jsonify({"msg": "Completed"})
    
    
# DELETING PLANET (BY ID) WITH DELETE METHOD
@app.route('/planets/<int:planets_id>', methods=['DELETE'])
def delete_planet(planets_id):
    single_planet = Planets.query.get(planets_id) # Checks if planets id exists
    if single_planet is None:
        raise APIException("That planet does not exists!", status_code=400)
    db.session.delete(single_planet)
    db.session.commit()
    return jsonify({"msg": "Completed"})

#GET ALL CHARACTERS
@app.route('/characters', methods=['GET'])
def get_characters():
    characters = Characters.query.all()
    characters_serialized = list(map(lambda x: x.serialize(), characters))
    return jsonify({"msg": 'Completed', "characters": characters_serialized})

# GET SINGLE CHARACTER
@app.route('/characters/<int:characters_id>', methods=['GET'])
def get_single_character(characters_id):
    single_character = Characters.query.get(characters_id)
    response_body = {
        "characters_id" : characters_id,
        "characters_info": single_character.serialize()
    }
    
    return jsonify(response_body)

# ADDING NEW CHARACTER WITH METHOD PUT
@app.route('/characters', methods=['PUT'])
def modify_character():
    body = request.get_json(silent = True)
    if body is None:
        raise APIException("Character info is required", status_code=400)
    if "id" not in body:
        raise APIException("An ID must be given", status_code=400)
    if "name" not in body:
        raise APIException("A name must be given", status_code=400)
    single_character = Characters.query.get(body['id'])
    single_character.name = body['name']
    db.session.commit()
    return jsonify({"msg": "Completed"})

# DELETING CHARACTER WITH METHOD DELETE
@app.route('/characters/<int:characters_id>', methods=['DELETE'])
def delete_character(characters_id):
    single_character = Characters.query.get(characters_id) # Checks if planets id exists
    if single_character is None:
        raise APIException("That planet does not exists!", status_code=400)
    db.session.delete(single_character)
    db.session.commit()
    return jsonify({"msg": "Completed"})

# CATEGORITES FOR FAVORITE LIST (PLANETS & CHARACTERS)
@app.route('/category', methods=['GET'])
def handle_category():
    if request.method == 'GET':
        category = Category.query.all()
        return jsonify([x.serialize() for x in category]), 200

 

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
