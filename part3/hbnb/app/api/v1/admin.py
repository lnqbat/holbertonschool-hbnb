from app.services import facade
from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

api = Namespace('admin', description='Admin operations')

user_model = api.model('User', {
    'email': fields.String(required=True, description='Email of the user'),
    'first_name': fields.String(required=True, description='Fist name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'password':fields.String(required=True, description='Password of th user'),
    'is_admin': fields.Boolean(required=True, description='Admin of the user')
})

@api.route('/')
class AdminUserCreate(Resource):
    @api.expect(user_model, validate=True)
    @api.doc('list_users')
    @api.response(200, 'Success', [user_model])
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def get(self):
        """
        List all users (admin only)
        """
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        users = facade.get_all_users()
        return [user.to_dict() for user in users], 200

    @api.doc('create_user_admin')
    @api.expect(user_model, validate=True)
    @api.response(201, 'User created', user_model)
    @api.response(400, 'Email already registered')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def post(self):
        """
        Create a new user (admin only)
        """
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        user_data = request.json
        email = user_data.get('email')

        if facade.get_user_by_email(email):
            return {'error': 'Email already registered'}, 400

        new_user = facade.create_user(user_data)
        return new_user.to_dict(), 201


@api.route('/users/<string:user_id>')
class AdminUserUpdate(Resource):
    @jwt_required()
    @api.expect(user_model, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(400, 'Email already in use')
    @api.response(404, 'User not found')
    @api.response(403, 'Admin privileges required')
    def put(self, user_id):
        """Update any user (admin only)"""
        claims = get_jwt()
        if not claims.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        data = request.get_json()
        email = data.get('email')
        if email:
            existing_user = facade.get_user_by_email(email)
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email already in use'}, 400

        updated_user = facade.update_user(user_id, data)
        if not updated_user:
            return {'error': 'User not found'}, 404

        if data.get('password'):
            updated_user.hash_password(data['password'])

        return updated_user.to_dict(), 200

@api.route('/amenities/')
class AdminAmenityCreate(Resource):
    @jwt_required()
    @api.response(201, 'Amenity created successfully')
    @api.response(403, 'Admin privileges required')
    def post(self):
        """Create a new amenity (admin only)"""
        claims = get_jwt()
        if not claims.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        data = request.get_json()
        amenity = facade.create_amenity(data)
        return {'id': amenity.id, 'name': amenity.name}, 201

@api.route('/amenities/<string:amenity_id>')
class AdminAmenityUpdate(Resource):
    @jwt_required()
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(403, 'Admin privileges required')
    def put(self, amenity_id):
        """Update an amenity (admin only)"""
        claims = get_jwt()
        if not claims.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        data = request.get_json()
        amenity = facade.update_amenity(amenity_id, data)
        if not amenity:
            return {'message': 'Amenity not found'}, 404
        return {'message': 'Amenity updated successfully'}, 200
