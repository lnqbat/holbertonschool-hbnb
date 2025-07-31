from app.persistence.UserRepository import UserRepository
from app.persistence.repository import AmenityRepository, SQLAlchemyRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from app import db

class HBnBFacade:
    def __init__(self, user_repository=None, place_repository=None, review_repository=None, amenity_repository=None):
        self.user_repository = user_repository or UserRepository()
        self.place_repository = place_repository or SQLAlchemyRepository(Place)
        self.review_repository = review_repository or SQLAlchemyRepository(Review)
        self.amenity_repository = amenity_repository or SQLAlchemyRepository(Amenity)

# Users
    def create_user(self, user_data):
        user = User(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email=user_data['email'],
            password=user_data.get("password"),
            hashed=user_data.get("hashed", False)
        )
        user.is_admin = user_data.get("is_admin", False)
        self.user_repository.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repository.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repository.get_user_by_email(email)
    
    def update_user(self, user_id, update_data):
        return self.update(user_id, update_data)

    def update(self, user_id, update_data):
        user = self.get_user(user_id)
        if not user:
            return None

        if "email" in update_data:
            new_email = update_data["email"]
            existing_user = self.user_repository.get_user_by_email(new_email)
            if existing_user and existing_user.id != user.id:
                raise ValueError("Email already registered to another user")

        for key, value in update_data.items():
            if hasattr(user, key):
                if key == "password":
                    user.hash_password(value)
                else:
                    setattr(user, key, value)

        db.session.commit()
        return user
    
    def get_all_users(self):
        return self.user_repository.get_all()

    def delete_user(self, user_id):
        return self.user_repository.delete(user_id)

# Amenity
    def create_amenity(self, data):
        amenity = Amenity(name=data['name'])
        self.amenity_repository.add(amenity)
        return amenity

    def get_all_amenities(self):
        return self.amenity_repository.get_all()

    def get_amenity(self, amenity_id):
        return self.amenity_repository.get(amenity_id)

    def update_amenity(self, amenity_id, data):
        return self.amenity_repository.update(amenity_id, data)

    def delete_amenity(self, amenity_id):
        return self.amenity_repository.delete(amenity_id)

# Place
    def create_place(self, place_data):
        price = place_data.get('price')
        latitude = place_data.get('latitude')
        longitude = place_data.get('longitude')

        if price is None or price < 0:
            raise ValueError("Price must be a non-negative float.")
        if latitude is None or not (-90 <= latitude <= 90):
            raise ValueError("Latitude must be between -90 and 90.")
        if longitude is None or not (-180 <= longitude <= 180):
            raise ValueError("Longitude must be between -180 and 180.")

        owner_id = place_data.get('owner_id')
        owner = self.user_repository.get(owner_id)
        if not owner:
            raise ValueError("The specified owner does not exist.")

        amenities_ids = place_data.get('amenities', [])
        amenities = []
        for amenity_id in amenities_ids:
            amenity = self.amenity_repository.get(amenity_id)
            if not amenity:
                raise ValueError(f"Amenity not found: {amenity_id}")
            amenities.append(amenity)

        place = Place(
            title=place_data['title'],
            price=price,
            latitude=latitude,
            longitude=longitude,
            owner=owner,
            description=place_data.get('description', "")
        )
        place.amenities = amenities
        self.place_repository.add(place)
        return place

    def get_place(self, place_id):
        place = self.place_repository.get(place_id)
        if not place:
            raise ValueError("Place not found.")
        return place

    def get_all_places(self):
        return self.place_repository.get_all()

    def update_place(self, place_id, place_data):
        if 'price' in place_data and place_data['price'] < 0:
            raise ValueError("Price must be a non-negative float.")
        if 'latitude' in place_data and not (-90 <= place_data['latitude'] <= 90):
            raise ValueError("Latitude must be between -90 and 90.")
        if 'longitude' in place_data and not (-180 <= place_data['longitude'] <= 180):
            raise ValueError("Longitude must be between -180 and 180.")

        if 'owner_id' in place_data:
            owner = self.user_repository.get(place_data['owner_id'])
            if not owner:
                raise ValueError("The specified owner does not exist.")
            place_data['owner'] = owner
            del place_data['owner_id']

        if 'amenities' in place_data:
            amenity_ids = place_data['amenities']
            amenities = []
            for amenity_id in amenity_ids:
                amenity = self.amenity_repository.get(amenity_id)
                if not amenity:
                    raise ValueError(f"Amenity not found: {amenity_id}")
                amenities.append(amenity)
            place_data['amenities'] = amenities

        return self.place_repository.update(place_id, place_data)

# Review
    def create_review(self, review_data):
        user = self.user_repository.get(review_data.get('user_id'))
        place = self.place_repository.get(review_data.get('place_id'))
        rating = review_data.get('rating')
        text = review_data.get('text')

        if not user:
            raise ValueError("The specified user does not exist.")
        if not place:
            raise ValueError("The specified place does not exist.")
        if rating is None or not (0 <= rating <= 5):
            raise ValueError("Rating must be between 0 and 5.")

        review = Review(text=text, rating=rating)
        review.user_id = user.id
        review.place_id = place.id
        self.review_repository.add(review)
        return review

    def get_review(self, review_id):
        review = self.review_repository.get(review_id)
        if not review:
            raise ValueError("Review not found.")
        return review

    def get_all_reviews(self):
        return self.review_repository.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.place_repository.get(place_id)
        if not place:
            raise ValueError("Place not found.")
        return place.reviews

    def update_review(self, review_id, data):
        if 'rating' in data and not (0 <= data['rating'] <= 5):
            raise ValueError("Rating must be between 0 and 5.")
        return self.review_repository.update(review_id, data)

    def delete_review(self, review_id):
        return self.review_repository.delete(review_id)

    def delete_place(self, place_id):
            place = self.place_repository.get(place_id)
            if not place:
                raise ValueError("Place not found")
            self.place_repository.delete(place_id)

    def get_review_by_user_and_place(self, user_id, place_id):
        return Review.query.filter_by(user_id=user_id, place_id=place_id).first()

    @staticmethod
    def get_places_by_owner(user_id):
        return Place.query.filter_by(user_id=user_id).all()

