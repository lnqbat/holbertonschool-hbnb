from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services import facade
from flask import request

api = Namespace('auth', description='Authentication operations')

login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

@api.route('/login')
class Login(Resource):
    @api.expect(login_model, validate=True)
    @api.response(200, 'Login successful')
    @api.response(401, 'Invalid credentials')
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        user = facade.get_user_by_email(email)

        if not user:
            return {"error": "Invalid credentials"}, 401

        if not user.verify_password(password):
            return {"error": "Invalid credentials"}, 401

        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={"is_admin": user.is_admin}
        )
        return {"access_token": access_token}, 200
