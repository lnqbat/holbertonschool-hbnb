from models import BaseModel

class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        """
        Review class.
        """
        if not text:
            raise ValueError("Review text is required")
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")
        if not isinstance(place, object) or not hasattr(place, 'id'):
            raise ValueError("Invalid place")
        if not isinstance(user, object) or not hasattr(user, 'id'):
            raise ValueError("Invalid user")

        self.text = text
        self.rating = rating
        self.place = place
        self.user = user
