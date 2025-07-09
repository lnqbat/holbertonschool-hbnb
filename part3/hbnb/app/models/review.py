from app import db
from app.models import BaseModel

class Review(BaseModel):
    __tablename__ = 'reviews'

    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    place_id = db.Column(db.Integer, db.ForeignKey('places.id'), nullable=False)

    def __init__(self, text, rating):
        super().__init__()
        if not text:
            raise ValueError("Text is required")
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")

        self.text = text
        self.rating = rating

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
        }
