from models import BaseModel

class Place(BaseModel):
    def __init__(self, title, price, latitude, longitude, owner, description=""):
        """
        Place class, which inherits from BaseModel.
        """
        if not title or len(title) > 100:
            raise ValueError("Invalid title")
        if price < 0:
            raise ValueError("Price must be positive")
        if not (-90.0 <= latitude <= 90.0):
            raise ValueError("Latitude out of range")
        if not (-180.0 <= longitude <= 180.0):
            raise ValueError("Longitude out of range")
        if not isinstance(owner, object) or not hasattr(owner, 'id'):
            raise ValueError("Invalid owner")

        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []
        self.amenities = []

    def add_review(self, review):
        self.reviews.append(review)

    def add_amenity(self, amenity):
        self.amenities.append(amenity)
