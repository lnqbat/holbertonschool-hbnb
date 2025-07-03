from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt, verify_jwt_in_request, get_jwt_identity
from app.services import facade

api = Namespace('admin', description='Admin operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})


@api.route('/')
class UserList(Resource):
    @jwt_required()
    @api.response(200, 'List of users retrieved successfully', [user_model])
    @api.response(403, 'Admin privileges required')
    def get(self):
        """ List all users (admin only) """
        claims = get_jwt()
        if not claims.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        users = facade.get_all_users()
        return [user.to_dict() for user in users], 200

    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created', user_model)
    @api.response(400, 'Email already registered')
    @api.response(403, 'Admin privileges required')
    def post(self):
        """ Create a new user (admin only after first user) """
        user_data = request.get_json()
        email = user_data.get('email')
        if facade.get_user_by_email(email):
            return {'error': 'Email already registered'}, 400

        if len(facade.get_all_users()) > 0:
            verify_jwt_in_request()
            claims = get_jwt()
            if not claims.get('is_admin'):
                return {'error': 'Admin privileges required'}, 403

        new_user = facade.create_user(user_data)
        password = user_data.get('password')
        if password:
            new_user.hash_password(password)

        return new_user.to_dict(), 201


@api.route('/<user_id>')
class UserResource(Resource):
    @jwt_required()
    @api.response(200, 'User details retrieved')
    @api.response(403, 'Not authorized')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """ Retrieve user by ID (self or admin) """
        claims = get_jwt()
        current_user = get_jwt_identity()

        if not claims.get('is_admin') and current_user != user_id:
            return {'error': 'Not authorized'}, 403

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return user.to_dict(), 200

    @jwt_required()
    @api.expect(user_model, validate=True)
    @api.response(200, 'User updated successfully')
    @api.response(403, 'Not authorized')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid or duplicate email')
    def put(self, user_id):
        """ Update user (self or admin) """
        claims = get_jwt()
        current_user = get_jwt_identity()

        if not claims.get('is_admin') and current_user != user_id:
            return {'error': 'Not authorized'}, 403

        data = api.payload
        email = data.get('email')
        if email:
            existing_user = facade.get_user_by_email(email)
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email already registered'}, 400

        updated_user = facade.update_user(user_id, data)
        if not updated_user:
            return {'error': 'User not found'}, 404
        return updated_user.to_dict(), 200
