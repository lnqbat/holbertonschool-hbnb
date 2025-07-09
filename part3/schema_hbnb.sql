CREATE TABLE users (
    id CHAR(36) PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE
);

CREATE TABLE places (
    id CHAR(36) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    owner_id CHAR(36) NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES users(id)
);

CREATE TABLE reviews (
    id CHAR(36) PRIMARY KEY,
    text TEXT NOT NULL,
    rating INT CHECK(rating >= 1 AND rating <= 5) NOT NULL,
    user_id CHAR(36) NOT NULL,
    place_id CHAR(36) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (place_id) REFERENCES places(id),
    UNIQUE(user_id, place_id)
);

CREATE TABLE amenities (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE place_amenity (
    place_id CHAR(36),
    amenity_id CHAR(36),
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCES places(id),
    FOREIGN KEY (amenity_id) REFERENCES amenities(id)
);


INSERT INTO "User" (id, first_name, last_name, email, password, is_admin)
VALUES 
('36c9050e-ddd3-4c3b-9731-9f487208bbc1', 'Admin', 'HBnB', 'admin@hbnb.io',
 '$2b$12$1m2epwOe16MN9tZp6GZ2vuqEEXyhb8H5i3R6rz86kJ83lmURylY7i', TRUE);

INSERT INTO Amenity (id, name)
VALUES 
('7cf1b8e7-3e77-41ad-96d1-8d8fa1a3f9a1', 'WiFi'),
('5ba91e3e-74b6-414c-bb83-1827c56a0c71', 'Swimming Pool'),
('3dd05af1-30a2-4c1d-9b25-5283e1ee6f89', 'Air Conditioning');