# 🏠 HBnB - API REST

<p align="center">
  <img src="https://github.com/lnqbat/holbertonschool-hbnb/blob/main/part1/image/HBNB.png" alt="Logo du projet" width="250"/>
</p>

RESTful API to manage entities in the HBnB project: `User`, `Place`, `Review`, `Amenity`. Built with a layered architecture (Presentation, Business Logic, Persistence) using Flask-RESTx.

## 📜 Summary

- [Installation](#️-installation)
- [Start the API](#️-start-the-api)
- [Available Endpoints](#-available-endpoints)
    - [Users](#-users)
    - [Places](#-places)
    - [Reviews](#-reviews)
    - [Amenities](#-amenities)
- [Quick Example](#-quick-example)
- [Features](#-features)

## ⚙️ Installation

```bash
git clone https://github.com/lnqbat/holbertonschool-hbnb.git
cd part2
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## ▶️ Start the API

```bash
python3 run.py
```

API is available at: `http://localhost:5000/`

## 📌 Available Endpoints

### 🔹 Users

| Method | Route             | Description                |
|--------|-------------------|----------------------------|
| POST   | `/users`          | Create a new user          |
| GET    | `/users`          | Retrieve all users         |
| GET    | `/users/<id>`     | Retrieve a user by ID      |
| PUT    | `/users/<id>`     | Update an existing user    |

### 🔹 Places

| Method | Route              | Description                |
|--------|--------------------|----------------------------|
| POST   | `/places`          | Create a new place         |
| GET    | `/places`          | Retrieve all places        |
| GET    | `/places/<id>`     | Retrieve a place by ID     |
| PUT    | `/places/<id>`     | Update an existing place   |

### 🔹 Reviews

| Method | Route               | Description                 |
|--------|---------------------|-----------------------------|
| POST   | `/reviews`          | Create a new review         |
| GET    | `/reviews`          | Retrieve all reviews        |
| GET    | `/reviews/<id>`     | Retrieve a review by ID     |
| PUT    | `/reviews/<id>`     | Update an existing review   |

### 🔹 Amenities

| Method | Route                | Description                     |
|--------|----------------------|---------------------------------|
| POST   | `/amenities`         | Create a new amenity            |
| GET    | `/amenities`         | Retrieve all amenities          |
| GET    | `/amenities/<id>`    | Retrieve an amenity by ID       |
| PUT    | `/amenities/<id>`    | Update an existing amenity      |

## 📤 Quick Example

```bash
curl -X POST http://localhost:5000/users \
-H "Content-Type: application/json" \
-d '{"email": "alice@mail.com", "first_name": "Alice"}'
```
s
## ✅ Features

- RESTful API using Flask-RESTx
- Clear 3-layer architecture
- Strong business logic validation
- Simple and extensible in-memory persistence
