from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_restx import Api

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    from app.api.v1.users import api as users_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.places import api as place_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.auth import api as auth_ns
    from app.api.v1.admin import api as admin_users

    authorizations = {
        'Bearer Auth': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': "Add a JWT with **Bearer <JWT>**"
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

    with app.app_context():
        db.create_all()

        from app.models.user import User
        admin = User.query.filter_by(email="admin@hbnb.io").first()
        if not admin:
            hashed_pw = bcrypt.generate_password_hash("admin1234").decode()
            admin = User(
                first_name="Admin",
                last_name="HBnB",
                email="admin@hbnb.io",
                password=hashed_pw,
                is_admin=True,
                hashed=True
            )
            db.session.add(admin)
            db.session.commit()
        else:
            changed = False
            if not admin.is_admin:
                admin.is_admin = True
                changed = True
            if not admin.verify_password("admin1234"):
                admin.hash_password("admin1234")
                changed = True
            if changed:
                db.session.commit()

    return app
