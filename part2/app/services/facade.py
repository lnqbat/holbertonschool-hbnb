from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity

class HBnBFacade:
    def __init__(self, user_repository=None, place_repository=None, review_repository=None, amenity_repository=None):
        self.user_repository = user_repository
        self.place_repository = place_repository
        self.review_repository = review_repository
        self.amenity_repository = amenity_repository

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repository.add(user)
        return user

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

    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repository.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repository.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repository.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repository.get(amenity_id)
        if not amenity:
            return None
        for key, value in amenity_data.items():
            if hasattr(amenity, key):
                setattr(amenity, key, value)
        return amenity
