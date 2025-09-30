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
from models import db, User, Item, Pokemon, Favorite
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

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200



#GET de usuarios y usuario

@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    print(users)
    return jsonify([u.serialize() for u in users])

@app.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.serialize())


#GET de items e item

@app.route("/items", methods=["GET"])
def get_items():
    items = Item.query.all()
    print(items)
    return jsonify([i.serialize() for i in items])

@app.route("/items/<int:id>", methods=["GET"])
def get_item(id):
    item = Item.query.get_or_404(id)
    return jsonify(item.serialize())

#GET de pokemons y pokemon

@app.route("/pokemons", methods=["GET"])
def get_pokemons():
    pokemons = Pokemon.query.all()
    print(pokemons)
    return jsonify([p.serialize() for p in pokemons])

@app.route("/pokemons/<int:id>", methods=["GET"])
def get_pokemon(id):
    pokemon = Pokemon.query.get_or_404(id)
    return jsonify(pokemon.serialize())



#favorite

@app.route("/favorites", methods=["GET"])
def get_favorites():
    favorites = Favorite.query.all()
    return jsonify([f.serialize() for f in favorites])

@app.route("/favorites/user/<int:user_id>", methods=["GET"])
def get_favorites_by_user(user_id):
    favorites = Favorite.query.filter_by(user_id=user_id).all()
    return jsonify([f.serialize() for f in favorites])



@app.route("/favorites", methods=["POST"])
def create_favorite():
    data = request.get_json()

    user_id = data.get("user_id")
    pokemon_id = data.get("pokemon_id")
    item_id = data.get("item_id")

    if not user_id:
        return jsonify({"error": "Falta el user_id"}), 400

    if not pokemon_id and not item_id:
        return jsonify({"error": "Debes enviar al menos un pokemon_id o item_id"}), 400

    favorite = Favorite(
        user_id=user_id,
        pokemon_id=pokemon_id,
        item_id=item_id
    )

    db.session.add(favorite)
    db.session.commit()

    return jsonify(favorite.serialize()), 201


@app.route("/favorites/<int:id>", methods=["DELETE"])
def delete_favorite(id):
    favorite = Favorite.query.get_or_404(id)

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"message": "Favorito eliminado"}), 200



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
