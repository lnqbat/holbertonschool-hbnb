from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask import request
from flask_jwt_extended import jwt_required, get_jwt, verify_jwt_in_request, get_jwt_identity

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
        """Create a new user"""
        user_data = request.get_json()
        if facade.get_user_by_email(user_data['email']):
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
    def get(self, user_id):
        """ Retrieve user by ID (owner or admin) """
        claims = get_jwt()
        if not claims.get('is_admin') and get_jwt_identity() != user_id:
            return {'error': 'Not authorized'}, 403

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return user.to_dict(), 200

    @jwt_required()
    @api.expect(user_model, validate=True)
    def put(self, user_id):
        """ Update user (owner or admin) """
        claims = get_jwt()
        if not claims.get('is_admin') and get_jwt_identity() != user_id:
            return {'error': 'Not authorized'}, 403

        update_data = api.payload
        updated_user = facade.update_user(user_id, update_data)
        if not updated_user:
            return {'error': 'User not found'}, 404
        return updated_user.to_dict(), 200
