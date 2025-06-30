from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade
from app.services import facade
from flask import request

api = Namespace('places', description='Place operations')

amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})


place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """ Register a new place """
        data = api.payload
        try:
            place = facade.create_place(data)
            return place.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """ Retrieve all places """
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        owner_id = request.args.get('owner_id')

        places = facade.get_all_places()

        if min_price is not None:
            places = [p for p in places if p.price >= min_price]
        if max_price is not None:
            places = [p for p in places if p.price <= max_price]
        if owner_id:
            places = [p for p in places if p.owner_id == owner_id]

        return [place.to_dict() for place in places], 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """ Retrieve a place by ID """
        try:
            place = facade.get_place(place_id)
            owner = place.owner

            amenities = [
                {
                    "id": str(am.id),
                    "name": am.name
                }
                for am in place.amenities
            ]

            result = {
                "id": str(place.id),
                "title": place.title,
                "description": place.description,
                "latitude": place.latitude,
                "longitude": place.longitude,
                "owner": {
                    "id": str(owner.id),
                    "first_name": owner.first_name,
                    "last_name": owner.last_name,
                    "email": owner.email
                },
                "amenities": amenities
            }

            return result, 200
        except ValueError as e:
            return {'error': str(e)}, 404

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """ Update place """
        data = api.payload
        try:
            place = facade.update_place(place_id, data)
            return {"message": "Place updated successfully"}, 200
        except ValueError as e:
            return {'error': str(e)}, 404
        except Exception as e:
            return {'error': str(e)}, 400