from app import db
from app.models import BaseModel

class Amenity(BaseModel):
    __tablename__ = 'amenities'

    name = db.Column(db.String(100), nullable=False)

    def __init__(self, name):
        """
        Amenity class.
        """
        super().__init__()
        self.name = name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }
 