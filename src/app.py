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
from models import db, User, People, Planets, UserFavoritePlanets 


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
    # create a list
    results = []
    for planet in planet:
       results.append(planet.serialize())    
    response_body = {'message': 'Ok',
                     'total_records': len(results),
                     'results':results}
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
       favorite_planets = db.get_or_404(UserFavoritePlanets, user_id)
       results = favorite_planets.serialize()
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

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)



    