from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.persistence.repository import AmenityRepository


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
