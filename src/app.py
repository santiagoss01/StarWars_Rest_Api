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
from models import db, User, People, Planets, UserFavoritePlanets, UserFavoritePeople 


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


@app.route('/user', methods=['GET'])
def get_user():
    users = User.query.all()
    # create a list
    results = []
    for user in users:
       results.append(user.serialize())
    response_body = {
        'message': 'Ok',
        'total_records': len(results),
        'results':results
    }

    return jsonify(response_body), 200


@app.route('/user', methods=['POST'])
def post_user():
    request_body: request.get_json()
    user =  User(email = request_body['email'],
                 password = request_body['password'],
                 is_active = request_body['is_active'])
    db.session.add(User),
    db.session.commit
    return jsonify(request_body), 200


@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    request_body = request.get_json()
    user = User.query.get(user_id)
    if user is None:
       raise APIException('User not found', status_code=404)
    if "email" in request_body:
       user.email = request_body["email"] 
    db.session.commit()
    return jsonify(request_body), 200


@app.route('/people', methods=['GET'])
def get_people():
    peoples = People.query.all()
    # create a list
    results = []
    for people in peoples:
       results.append(people.serialize())    
    response_body = {'message': 'Ok',
                     'total_records': len(results),
                     'results':results}
    return jsonify(response_body), 200


@app.route("/people/<int:people_id>")
def people_by_id(people_id):

       people = db.get_or_404(People, people_id)
       results = people.serialize()
       response_body = {'message': 'Ok',
                     'total_records': len(results),
                     'results':results}
       return jsonify(response_body), 200


@app.route('/planets', methods=['GET'])
def get_planet():
    planet = Planets.query.all()
    results = [planet.serialize() for planet in planets]
    response_body = {"message": "ok",
                     "total_records": len(results),
                     "results": results}
    return jsonify(response_body), 200


@app.route("/planets/<int:planets_id>")
def planet_by_id(planets_id):
       planet = db.get_or_404(Planets, planets_id)
       results = planet.serialize()
       response_body = {'message': 'Ok',
                     'total_records': len(results),
                     'results':results}
       return jsonify(response_body), 200


@app.route('/user/favorite-planets/<int:user_id>', methods=['GET'])
def get_favorite_planet(user_id):
       favorites = UserFavoritePlanets.query.filter(UserFavoritePlanets.user_id == user_id).all()
       results = [favorite.serialize() for favorite in favorites]
       response_body = {'message': 'Ok',
                        'total_records': len(results),
                        'results':results}
       return jsonify(response_body), 200

@app.route('/favorite/planets', methods=['POST'])
def post_favorite_planet():
        
         request_body = request.get_json()
         favorite =  UserFavoritePlanets( user_id = request_body['user_id'],
                                          favorite_planet_id = request_body ['favorite_planet_id'])
         db.session.add(favorite),
         db.session.commit()
         return jsonify(request_body), 200


@app.route("/user/favorites-planets/<int:favorite_id>", methods = ["DELETE"])
def delete_favorite_planet(favorite_id):
    favorites = UserFavoritesPlanets.query.get(favorite_id)
    if favorites is None:
        raise APIException('Favorite not found', status_code=404)
    db.session.delete(favorites)
    db.session.commit()
    return jsonify("Ok"), 200


@app.route('/user/favorites-people/<int:user_id>', methods=['GET'])
def get_favorites_people(user_id):
    favorites = UserFavoritePeople.query.filter(UserFavoritePeople.user_id == user_id).all()
    results = [favorite.serialize() for favorite in favorites]
    response_body = {"message": "ok",
                     "total_records": len(results),
                     "results": results}
    return jsonify(response_body), 200


@app.route('/favorite/people', methods=['POST'])
def add_favorites_people():
    request_body = request.get_json()
    favorite = UserFavoritePeople(user_id = request_body['user_id'],
                                  favorite_people_id = request_body['favorite_people_id'])
    db.session.add(favorite)
    db.session.commit()
    return jsonify(request_body), 200


@app.route("/user/favorites-people/<int:favorite_id>", methods = ["DELETE"])
def delete_favorite_people(favorite_id):
    favorites = UserFavoritePeople.query.get(favorite_id)
    if favorites is None:
        raise APIException('Favorite not found', status_code=404)
    db.session.delete(favorites)
    db.session.commit()
    return jsonify("Ok"), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)



    