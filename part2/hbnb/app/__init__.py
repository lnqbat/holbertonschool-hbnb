from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as place_ns
from app.api.v1.reviews import api as reviews_ns

bcrypt = Bcrypt()

def create_app(config_class="config.DevelopmentConfig"):
    app= Flask(__name__)
    app.config.from_object(config_class)

    bcrypt.init_app(app)

    api= Api(app, version= '1.0', title= 'HBnB API', description= 'HBnB Application API',)

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path="/api/v1/amenities")
    api.add_namespace(place_ns, path="/api/v1/places")
    api.add_namespace(reviews_ns, path="/api/v1/reviews")

    return app
