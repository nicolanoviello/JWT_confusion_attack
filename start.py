from flask import jsonify
from flask import Flask
from flask_restful import Api
jwt_app = Flask(__name__)
jwt_api = Api(jwt_app)
from flask_sqlalchemy import SQLAlchemy

# Definisco i miei parametri di environment per il db e per la secret
jwt_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jwt_app.db'
jwt_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
jwt_app.config['SECRET_KEY'] = 'abc'

# Instanzio il db
db = SQLAlchemy(jwt_app)

# Inizializzo il db prima di eseguire qualsiasi altra cosa
@jwt_app.before_first_request

def create_tables():
    db.create_all()

import resources,models
# Mappo le risorse su specifici endpoint
jwt_api.add_resource(resources.Registration, '/registration')
jwt_api.add_resource(resources.Login, '/login')
jwt_api.add_resource(resources.ListaUtenti, '/users')
jwt_api.add_resource(resources.CheckJWT, '/scopriruolo')




