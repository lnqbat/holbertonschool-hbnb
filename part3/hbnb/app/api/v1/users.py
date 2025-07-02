from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask import request
from flask_jwt_extended import jwt_required, get_jwt, verify_jwt_in_request

api = Namespace('users', description='User operations')

user_model = api.model('User', {
     'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password':fields.String(required=True, description='Password of th user')
 })

@api.route('/')
class UserList(Resource):
    @jwt_required()
    @api.response(200, 'List of users retrieved successfully', [user_model])
    @api.response(403, 'Admin privileges required')
    def get(self):
        """List all users (admin only)"""
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
        """Create a new user (admin only)"""
        if len(facade.get_all_users()) > 0:
            verify_jwt_in_request()
            claims = get_jwt()
            if not claims.get('is_admin'):
                return {'error': 'Admin privileges required'}, 403

        user_data = request.get_json()
        if facade.get_user_by_email(user_data['email']):
            return {'error': 'Email already registered'}, 400

        new_user = facade.create_user(user_data)
        password = user_data.get('password')
        if password:
            new_user.hash_password(password)

        return new_user.to_dict(), 201

@api.route('/<user_id>')
class UserResource(Resource):
    @jwt_required()
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """ Retrieve user by ID """
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200

    @api.expect(user_model, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    def put(self, user_id):
        """ Update user """
        update_data = api.payload
        updated_user = facade.update_user(user_id, update_data)
        if not updated_user:
            return {'error': 'User not found'}, 404

        return updated_user.to_dict(), 200
