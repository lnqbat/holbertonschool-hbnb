# 🏠 HBnB – Final Project

This is the final version of the **HBnB full-stack project**, inspired by Airbnb. It features a layered backend architecture built with Flask (REST API), a dynamic frontend in HTML/CSS/JS.

---

## 📌 Table of Contents

- [📁 Project Structure](#-project-structure)
- [🚀 How to Run the Project](#-how-to-run-the-project)
  - [1. Clone the repository](#1-clone-the-repository)
  - [2. Backend Setup (API)](#2-backend-setup-api)
  - [3. Frontend Setup](#3-frontend-setup)
    - [Open the main page manually](#open-the-main-page-manually)
- [✨ Main Features](#-main-features)
- [🧪 API Testing](#-api-testing)
- [📜 Notes](#-notes)
- [👨‍💻 Author](#-author)



## 📁 Project Structure

```
part4/
├── hbnb/
│   └── app/
│       ├── api/v1/            # API route controllers
│       ├── models/            # Business entities: User, Place, Review, Amenity
│       ├── persistence/       # In-memory repository (can be swapped later)
│       └── services/          # Business logic layer (facade)
├── base_files/                # Frontend files
│   ├── index.html
│   ├── place.html
│   ├── login.html
│   ├── register.html
│   ├── my-places.html
│   ├── add-review.html
│   ├── scripts.js
│   └── styles.css
├── run.py                     # Main backend entry point
├── requirements.txt           # Python dependencies
├── schema_hbnb.sql            # Optional DB schema
└── README.md
```

---

## 🚀 How to Run the Project

### 1. Clone the repository

```bash
git clone https://https://github.com/lnqbat/holbertonschool-hbnb
cd part4/hbnb
```

---

### 2. Backend Setup (API)

#### ✅ Prerequisites

- Python 3.8+
- `pip` and `venv` installed

#### 🔧 Install dependencies

```bash
python3 -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### ▶️ Start the backend server

```bash
python run.py
```

The API will be running on: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

### 3. Frontend Setup

No build step needed — it's pure HTML/CSS/JS.

#### Open the main page manually:

```bash
cd base_files/
```
And run 
```
python3 -m http.server
```
> ✅ The frontend makes requests to the backend running on `http://localhost:8000`.

---

## ✨ Main Features

- 🔐 **Authentication** with JWT (register, login, logout)
- 🏘️ **Places** list and details view
- ✍️ **Add reviews** for logged-in users
- 🧾 **"My Places"** section (only your own)
- 🎯 **Frontend logic** in `scripts.js` with dynamic DOM

---

## 🧪 API Testing

You can test the API using Postman or `curl`. Example: register a user

```bash
curl -X POST http://127.0.0.1:5000/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{"first_name": "Alice", "last_name": "Smith", "email": "alice@example.com", "password": "secure123"}'
```

---

## 📜 Notes

- All data is currently **in-memory** (non-persistent after restart).
- You can extend the repository layer for SQL/NoSQL persistence later.
- Make sure your browser allows JS to make requests to `localhost:8000`.

---

## 👨‍💻 Author

- 💡 Created as part of Holberton School Final Project
- ✉️ Baptiste Lonqueu – [GitHub](https://github.com/lnqbat)
