from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as place_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.auth import api as auth_ns
from app.api.v1.admin import api as admin_users

bcrypt = Bcrypt()
jwt = JWTManager()
db = SQLAlchemy()

def seed_users():
        from app.services import facade
        email = "admin@example.com"
        user = facade.get_user_by_email(email)
        if not user:
            hashed_pw = bcrypt.generate_password_hash("adminpassword").decode("utf-8")
            user = facade.create_user({
                "first_name": "Admin",
                "last_name": "Root",
                "email": email,
                "password": hashed_pw,
                "hashed": True
            })
            user.is_admin = True
            print(f"Seeded user: {user.email}")
        else:
            print(f"User already exists: {user.email}")

def create_app(config_class="config.DevelopmentConfig"):
    app= Flask(__name__)
    app.config.from_object(config_class)
    jwt.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)

    authorizations = {
        'Bearer Auth': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': "Add a JWT with **Bearer &lt;JWT&gt;**"
        }
    }

    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        authorizations=authorizations,
        security='Bearer Auth'
    )

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path="/api/v1/amenities")
    api.add_namespace(place_ns, path="/api/v1/places")
    api.add_namespace(reviews_ns, path="/api/v1/reviews")
    api.add_namespace(auth_ns, path="/api/v1/auth")
    api.add_namespace(admin_users, path="/api/v1/admin/users")

    seed_users()
    return app
