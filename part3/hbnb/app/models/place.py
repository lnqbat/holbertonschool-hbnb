from app import db
from app.models import BaseModel

place_amenity = db.Table('place_amenity',
    db.Column('place_id', db.Integer, db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.Integer, db.ForeignKey('amenities.id'), primary_key=True)
)

class Place(BaseModel):
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    reviews = db.relationship('Review', backref='place', lazy=True)
    amenities = db.relationship('Amenity', secondary='place_amenity', back_populates='places')

    def __init__(self, title, price, latitude, longitude, owner, description=""):
        super().__init__()
        if not title or len(title) > 100:
            raise ValueError("Invalid title")
        if price < 0:
            raise ValueError("Price must be positive")
        if not (-90.0 <= latitude <= 90.0):
            raise ValueError("Latitude out of range")
        if not (-180.0 <= longitude <= 180.0):
            raise ValueError("Longitude out of range")
        if not hasattr(owner, 'id'):
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

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner.id if hasattr(self.owner, 'id') else None,
            'amenities': [a.id for a in self.amenities],
            'created_at': self.created_at.isoformat() if hasattr(self, 'created_at') else None,
        }
