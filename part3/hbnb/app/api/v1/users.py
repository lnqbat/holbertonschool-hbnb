from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User created successfully')
    @api.response(400, 'Email already registered')
    def post(self):
        """Public endpoint: create a user"""
        data = request.get_json()
        if facade.get_user_by_email(data.get("email")):
            return {"error": "Email already registered"}, 400
        user = facade.create_user(data)
        return user.to_dict(), 201

@api.route('/<string:user_id>')
class UserProfile(Resource):
    @api.response(200, 'User retrieved successfully')
    @api.response(403, 'Not authorized')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Retrieve own profile"""
        user = facade.get_user(user_id)
        if not user:
            return {"error": "User not found"}, 404
        return user.to_dict(), 200

    @api.expect(user_model, validate=True)
    @api.response(200, 'Profile updated successfully')
    @api.response(403, 'Not authorized')
    @api.response(404, 'User not found')
    @jwt_required()
    def put(self, user_id):
        """Update own profile or admin update"""
        identity = get_jwt_identity()
        claims = get_jwt()
        if identity != user_id and not claims.get("is_admin"):
            return {"error": "Not authorized"}, 403
        try:
            user = facade.update_user(user_id, api.payload)
        except ValueError as e:
            return {"error": str(e)}, 400
        if not user:
            return {"error": "User not found"}, 404
        return user.to_dict(), 200

    @api.response(200, 'User deleted successfully')
    @api.response(403, 'Not authorized')
    @api.response(404, 'User not found')
    @jwt_required()
    def delete(self, user_id):
        """Delete own profile or admin delete"""
        identity = get_jwt_identity()
        claims = get_jwt()
        if identity != user_id and not claims.get("is_admin"):
            return {"error": "Not authorized"}, 403
        try:
            facade.delete_user(user_id)
            return {"message": "User deleted successfully"}, 200
        except ValueError as e:
            return {"error": str(e)}, 404
        except Exception as e:
            return {"error": str(e)}, 400
