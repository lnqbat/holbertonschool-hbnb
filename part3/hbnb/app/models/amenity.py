from app import db
from app.models import BaseModel

class Amenity(BaseModel):
    __tablename__ = 'amenities'

    name = db.Column(db.String(100), nullable=False)

    places = db.relationship('Place', secondary='place_amenity', back_populates='amenities')

    def __init__(self, name):
        super().__init__()
        self.name = name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat() if hasattr(self, 'created_at') else None
        }
