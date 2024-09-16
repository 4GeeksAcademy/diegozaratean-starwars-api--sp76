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
from models import db, User, Empresa
#from models import Person

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

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

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret deberian colcoar cualquier cosa"  # Change this!
# palabraa.  diegoa.   casaa
# palabraaaron
# palabra ===> asfasdfasdfasdfasdfkqewrkewjrjwehrkejwhrkj
# palabra ===> papalapabrapa

jwt = JWTManager(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

## INCION CODIGO

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():
    print('estoy debuguenado')
    all_users = User.query.all()
    print(all_users)
    results = list(map(lambda usuario: usuario.serialize() ,all_users)) 
    print(results)
    response_body = {
        "msg": "Hello, this is your GET /user response 123 "
    }

    return jsonify(results), 200

@app.route('/company', methods=['GET'])
@jwt_required()
def get_companies():
    all_companies = Empresa.query.all()
    results = list(map(lambda company: company.serialize() ,all_companies)) 

    return jsonify(results), 200

@app.route('/company/<int:company_id>', methods=['GET'])
def get_company(company_id):
    company = Empresa.query.filter_by(id=company_id).first()

    return jsonify(company.serialize()), 200

@app.route('/company', methods=['POST'])
def create_company():
    # DONE validacion modelo
    # DONE leer las variables del body

    print(request)
    print(request.get_json())
    body = request.get_json()

    if 'ciudad' not in body:
        return jsonify('debes enviarme la ciduad'), 400
    if body['ciudad'] == '':
        return jsonify('La ciudad no puede ser vacia'), 400


    print(request.get_json()['ciudad'])
    # crear la compañia en la DB
    company = Empresa(**body)
    db.session.add(company)
    db.session.commit()

    response_body = {
        "msg": "cree una nueva empresa"
    }

    return jsonify(response_body), 200


@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    user = User.query.filter_by(email=email).first()
    if user is None:
        return jsonify({"msg": "user not found"}), 401
    print(user)
    print(user.password)
    if user.password != password:
        return jsonify({"msg": "wrong passwaord"}), 401


    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token)


@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


## FIN CODIGO

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
