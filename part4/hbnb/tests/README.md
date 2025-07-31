# ✅ Testing and Validation Report – HBnB API

This document summarizes the implementation and validation of endpoints for the HBnB API project. It includes the validation logic, manual testing using cURL and Swagger, and automated testing using Python’s `unittest`.

---

## 📌 Objective

- Ensure all API endpoints behave correctly.
- Validate input data at the business logic level.
- Test all expected success and error scenarios (e.g. 201, 200, 400).
- Confirm consistency between implementation and documentation.

---

## ✅ Validation Implemented (Business Logic)

### 🧍 User
- `first_name`, `last_name`, `email` → must not be empty
- `email` must match a valid email format

### 🏠 Place
- `title` must not be empty
- `price` must be a positive number
- `latitude` must be between -90 and 90
- `longitude` must be between -180 and 180

### 📝 Review
- `text` must not be empty
- `user_id` and `place_id` must reference existing entities

### 🛏️ Amenity
- `name` must not be empty

---

## 🧪 Manual Testing with cURL

### ✔️ Valid User Creation

```bash
curl -X POST http://127.0.0.1:5000/api/v1/users/ \
-H "Content-Type: application/json" \
-d '{"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"}'
```

Expected: `201 Created`

### ❌ Invalid User Creation (Missing Data)

```bash
curl -X POST http://127.0.0.1:5000/api/v1/users/ \
-H "Content-Type: application/json" \
-d '{"first_name": "", "last_name": "", "email": "invalid-email"}'
```

Expected: `400 Bad Request`

### ❌ Invalid Place Latitude

```bash
curl -X POST http://127.0.0.1:5000/api/v1/places/ \
-H "Content-Type: application/json" \
-d '{"title": "Test", "price": 80, "latitude": 100, "longitude": 2.5}'
```

Expected: `400 Bad Request`

---

## 🧬 Swagger UI Verification

✅ Verified all models and routes via:
[http://127.0.0.1:5000/api/v1/](http://127.0.0.1:5000/api/v1/)

- All input fields and schemas are correctly represented.
- Error responses documented with example payloads.

---

## 🧪 Unit Tests Summary

### ✅ Files Used

- [`test_user.py`](https://github.com/lnqbat/holbertonschool-hbnb/blob/main/part2/hbnb/tests/test_user.py) (Create, GET, PUT user)
- [`test_place.py`](https://github.com/lnqbat/holbertonschool-hbnb/blob/main/part2/hbnb/tests/test_place.py) (Valid + Invalid creation)
- [`test_review.py`](https://github.com/lnqbat/holbertonschool-hbnb/blob/main/part2/hbnb/tests/test_review.py) (Create, GET, PUT review with user + place setup)
- [`test_amenity.py`](https://github.com/lnqbat/holbertonschool-hbnb/blob/main/part2/hbnb/tests/test_amenity.py) (Create, GET, PUT amenity)

### 🧪 Run the tests

```bash
python3 -m unittest discover -s tests
```

Expected:
```
...........
----------------------------------------------------------------------
Ran 11 tests in 0.042s

OK
```

---

## 📝 Observations

- Validation errors trigger correct HTTP status codes.
- Entity creation and updates behave as expected.
- One minor logic mismatch fixed in user update test (`first_name` assertion).

---

## ✅ Outcome

- [x] Validation added to all entity models
- [x] Endpoints tested manually and automatically
- [x] Swagger verified for accuracy
- [x] Tests confirm both success and edge cases
- [x] Full report written and ready
