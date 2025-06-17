from models import BaseModel

class Amenity(BaseModel):
    
    def __init__(self, name):
        """
        Amenity class.
        """
        if not name or len(name) > 50:
            raise ValueError("Invalid amenity name")
        self.name = name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }
