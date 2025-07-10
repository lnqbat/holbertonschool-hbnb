# 🏡 Holberton BnB – Partie 3 : API, Authentification & Base de Données

Bienvenue dans **HBnB – Part 3**, un projet Fullstack inspiré d'Airbnb, axé sur le **développement backend**.  
Cette étape vous fait passer d’une logique en mémoire à une application web RESTful complète, sécurisée, persistante et scalable.

---

## 📌 Sommaire

- [🔧 Objectifs](#-objectifs)
- [⚙️ Stack Technique](#️-stack-technique)
- [🧠 Concepts Clés](#-concepts-clés)
- [📐 Modèle de Données (ER Diagramme)](#-modèle-de-données-er-diagramme)
- [🔐 Authentification](#-authentification)
- [🛣️ API Endpoints](#️-api-endpoints)
- [🚀 Lancer l'application](#-lancer-lapplication)
- [📂 Structure du Projet](#-structure-du-projet)
- [📚 Ressources](#-ressources)
- [👨‍💻 Auteur](#-auteur)

---

## 🔧 Objectifs

- Implémenter une API REST conforme aux standards.
- Gérer les utilisateurs, droits d’accès et authentification via JWT.
- Hash sécurisé des mots de passe avec `bcrypt`.
- Mapper les entités avec SQLAlchemy.
- Établir des **relations complexes** : one-to-many, many-to-many.
- Générer un **diagramme ER Mermaid.js**.

---

## ⚙️ Stack Technique

| Technologie       | Usage                           |
|------------------|----------------------------------|
| **Python**       | Langage principal                |
| **Flask**        | Framework Web/API                |
| **Flask-RESTX**  | Documentation Swagger intégrée   |
| **Flask-Bcrypt** | Hash des mots de passe           |
| **Flask-JWT-Extended** | Authentification JWT     |
| **Flask-SQLAlchemy** | ORM pour SQLite/PostgreSQL |
| **Mermaid.js**   | Diagrammes ER markdown           |
| **UUID**         | Identifiants uniques             |

---

## 🧠 Concepts Clés

- 🔒 **JWT Auth** : sécurisation des endpoints.
- 👥 **RBAC** : contrôle d'accès par rôle (`user` / `admin`).
- 🧱 **Repository Pattern** : découplage entre logique métier et stockage.
- 🧩 **ORM** : mapping des entités vers des tables relationnelles.
- 🔄 **CRUD REST** : gestion complète des ressources.

---

## 📐 Modèle de Données (ER Diagramme)

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
    PLACE ||--o{ REVIEW : receives
    PLACE ||--o{ PLACE_AMENITY : has
    AMENITY ||--o{ PLACE_AMENITY : contains
