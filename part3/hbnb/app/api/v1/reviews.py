from flask import request
from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(required=True),
    'rating': fields.Integer(required=True, min=0, max=5),
    'user_id': fields.String(required=True),
    'place_id': fields.String(required=True)
})


@api.route('/')
class ReviewList(Resource):
    @jwt_required()
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        identity = get_jwt_identity()
        data = request.json

        place = facade.get_place(data.get("place_id"))
        if not place:
            return {"error": "Place not found"}, 404
        if place.owner_id == identity:
            return {"error": "You cannot review your own place"}, 400

        already_reviewed = facade.get_review_by_user_and_place(identity, data.get("place_id"))
        if already_reviewed:
            return {"error": "You have already reviewed this place"}, 400

        data["user_id"] = identity
        try:
            review = facade.create_review(data)
            return review.to_dict(), 201
        except ValueError as e:
            return {"error": str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """ Retrieve all review """
        reviews = facade.get_all_reviews()
        return [r.to_dict() for r in reviews], 200


@api.route('/<string:review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """ Retrieve a review by review_ID """
        try:
            review = facade.get_review(review_id)
            return review.to_dict(), 200
        except ValueError as e:
            api.abort(404, str(e))

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, user_id):
        identity = get_jwt_identity()
        claims = get_jwt()

        if identity != user_id and not claims.get("is_admin"):
            return {"error": "Unauthorized action"}, 403

        payload = api.payload or {}
        if "email" in payload or "password" in payload:
            return {"error": "You cannot modify email or password"}, 400

        try:
            user = facade.update_user(user_id, payload)
        except ValueError as e:
            return {"error": str(e)}, 400
        if not user:
            return {"error": "User not found"}, 404
        return user.to_dict(), 200

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """ Delete review """
        try:
            facade.delete_review(review_id)
            return {"message": "Review deleted successfully"}, 200
        except ValueError as e:
            api.abort(404, str(e))


@api.route('/places/<string:place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """ Retrieve a review by place ID """
        try:
            reviews = facade.get_reviews_by_place(place_id)
            return [r.to_dict() for r in reviews], 200
        except ValueError as e:
            api.abort(404, str(e))
