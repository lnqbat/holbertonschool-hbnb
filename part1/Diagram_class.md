```mermaid
classDiagram
    class BaseModel {
        +id : UUID
        +createdAt : Date
        +updatedAt : Date
        +save
        +delete
    }

    class User {
        +firstName : String
        +lastName : String
        +email : String
        +password : String
        +createUser
        +updateUser
        +deleteUser
        +authenticate
    }

    class Place {
        +userId : UUID
        +name : String
        +description : String
        +createPlace
        +updatePlace
        +deletePlace
        +searchPlace
    }

    class Review {
        +userId : UUID
        +placeId : UUID
        +text : String
        +createReview
        +updateReview
        +deleteReview
        +validateReview
    }

    class Amenity {
        +name : String
        +createAmenity
        +updateAmenity
        +deleteAmenity
    }

    BaseModel <|-- User
    BaseModel <|-- Place
    BaseModel <|-- Review
    BaseModel <|-- Amenity

    User --> "*" Place : creates
    Place --> "*" Review : has
    User --> "*" Review : writes
    Place --> "*" Amenity : includes
    Amenity --> "*" Place
