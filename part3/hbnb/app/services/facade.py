from app.persistence.repository import SQLAlchemyRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

class HBnBFacade:
    def __init__(self, user_repository=None, place_repository=None, review_repository=None, amenity_repository=None):
        self.user_repository = SQLAlchemyRepository(User)
        self.place_repository = place_repository
        self.review_repository = review_repository
        self.amenity_repository = amenity_repository
        self.store = {}
        self.reviews = {} 

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

    def get_by_id(self, entity_id):
        return self.store.get(str(entity_id))

    def get_user(self, user_id):
        return self.user_repository.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repository.get_by_attribute('email', email)

    def update_user(self, user_id, update_data):
        user = self.user_repository.get(user_id)
        if not user:
            return None
        for key, value in update_data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        return user

    def get_all_users(self):
        return self.user_repository.get_all()

    def get_by_id(self, entity_id):
        entity_id = str(entity_id)
        if entity_id in self.store:
            return self.store[entity_id]
        return None

    def delete_user(self, user_id):
        if not self.user_repository.delete(user_id):
            return False
        return True

    # Amenity methods
    def create_amenity(self, data):
        amenity = Amenity(name=data['name'])
        return self.amenity_repository.add(amenity)

    def get_all_amenities(self):
        return self.amenity_repository.get_all()

    def get_amenity(self, amenity_id):
        return self.amenity_repository.get(amenity_id)

    def update_amenity(self, amenity_id, data):
        return self.amenity_repository.update(amenity_id, data)

    def delete_amenity(self, amenity_id):
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None
        self.amenity_repository.delete(amenity_id)
        return True

    # Place methods
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


    def create_review(self, review_data):
        user_id = review_data.get('user_id')
        place_id = review_data.get('place_id')
        rating = review_data.get('rating')

        user = self.user_repository.get(user_id)
        if not user:
            raise ValueError("The specified user does not exist.")

        place = self.place_repository.get(place_id)
        if not place:
            raise ValueError("The specified place does not exist.")

        if rating is None or not (0 <= rating <= 5):
            raise ValueError("Rating must be between 0 and 5.")

        review = Review(
            text=review_data.get('text'),
            rating=rating,
            user=user,
            place=place
        )

        self.review_repository.add(review)
        return review

    def create_review(self, review_data):
        user_id = review_data.get('user_id')
        place_id = review_data.get('place_id')
        rating = review_data.get('rating')
        text = review_data.get('text')

        user = self.user_repository.get(user_id)
        place = self.place_repository.get(place_id)

        if not user:
            raise ValueError("The specified user does not exist.")
        if not place:
            raise ValueError("The specified place does not exist.")
        if rating is None or not (0 <= rating <= 5):
            raise ValueError("Rating must be between 0 and 5.")

        review = Review(text=text, rating=rating, user=user, place=place)
        self.reviews[review.id] = review
        return review

    def get_review(self, review_id):
        review = self.reviews.get(review_id)
        if not review:
            raise ValueError("Review not found.")
        return review

    def get_all_reviews(self):
        return list(self.reviews.values())

    def get_reviews_by_place(self, place_id):
        if not self.place_repository.get(place_id):
            raise ValueError("Place not found.")
        return [r for r in self.reviews.values() if r.place.id == place_id]

    def update_review(self, review_id, data):
        review = self.get_review(review_id)
        if 'text' in data:
            review.text = data['text']
        if 'rating' in data:
            rating = data['rating']
            if not (0 <= rating <= 5):
                raise ValueError("Rating must be between 0 and 5.")
            review.rating = rating
        return review

    def delete_review(self, review_id):
        if review_id not in self.reviews:
            raise ValueError("Review not found.")
        del self.reviews[review_id]
