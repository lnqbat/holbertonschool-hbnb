# 🏡 HBnB API – Part 3

A RESTful API for a simplified Airbnb-style platform, supporting secure user management, place listings, reviews, amenities, and admin features. Built using Flask, SQLAlchemy, and JWT.

---

## 📌 Table of Contents

- [🔧 Objectives](#-objectives)
- [⚙️ Tech Stack](#️-tech-stack)
- [🔐 Authentication & Security](#-authentication--security)
- [📐 Data Model (ER Diagram)](#-data-model-er-diagram)
- [👨‍💻 Authors](#-authors)

---

## 🔧 Objectives

✅ Secure user registration & login  
✅ Password hashing with bcrypt  
✅ JWT-based authentication  
✅ Admin role with special access  
✅ Full CRUD for Places, Reviews, Amenities  
✅ SQLAlchemy models and repositories  
✅ Raw SQL schema & seed data  
✅ Entity relationship diagram with Mermaid.js  

---

## ⚙️ Tech Stack

- Python 3.10  
- Flask + Flask-RESTX  
- Flask-JWT-Extended  
- Flask-Bcrypt  
- SQLAlchemy + Flask-SQLAlchemy  
- SQLite (dev) / PostgreSQL (prod)  
- Mermaid.js for ER diagram  

---

## 🔐 Authentication & Security

- Passwords are hashed using **bcrypt**  
- Auth is done with **JWT tokens** in headers  
- Admins can manage users, amenities, and override ownership rules  
- Users can only update their own data and create one review per place

---

## 📐 Data Model (ER Diagram)

```mermaid
---
config:
  theme: default
---
erDiagram
    USER {
        string id PK
        string first_name
        string last_name
        string email
        string password
        boolean is_admin
    }
    PLACE {
        string id PK
        string title
        string description
        float price
        float latitude
        float longitude
        string owner_id FK
    }
    REVIEW {
        string id PK
        string text
        int rating
        string user_id FK
        string place_id FK
    }
    AMENITY {
        string id PK
        string name
    }
    PLACE_AMENITY {
        string place_id PK, FK
        string amenity_id PK, FK
    }
    USER ||--o{ PLACE : owns
    USER ||--o{ REVIEW : writes
    PLACE ||--o{ REVIEW : has
    PLACE ||--o{ PLACE_AMENITY : links
    AMENITY ||--o{ PLACE_AMENITY : links

## Authors 💻

@Inqbat & @Iyed13tns