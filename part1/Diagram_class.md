```mermaid
classDiagram

class BaseModel {
    +id :
    +created_at : datetime
    +updated_at : datetime
    +save() : void
    +dict() : dict
}

class User {
    +email : str
    +first_name : str
    +last_name : str
    -password : str
    +save() : void
    +dict() : dict
    +get_places()
    +get_reviews()
}

class Place {
    +name : str
    +description : str
    +numb_rooms : int
    +numb_bathrooms : int
    +max_guest : int
    +price_by_night : int
    +latitude : float
    +longitude : float
    -user_id
    -city_id
    +save() : void
    +dict() : dict
    +get_amenities()
    +get_reviews()
}

class Review {
    +text : str
    -user_id
    -place_id
    +save() : void
    +dict() : dict
}

class Amenity {
    +name : str
    +save() : void
    +dict() : dict
}

%% Inheritance
User --|> BaseModel
Place --|> BaseModel
Review --|> BaseModel
Amenity --|> BaseModel

%% Associations
User --> Place
User --> Review
Place --> Review
Place --> Amenity
Review --> User
Review --> Place
