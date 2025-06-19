import unittest
from app import create_app

class TestReview(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

        # Create a user
        user_res = self.client.post('/api/v1/users/', json={
            "first_name": "ReviewTest",
            "last_name": "User",
            "email": "review.user@example.com"
        })
        self.user_id = user_res.get_json()["id"]

        # Create a place
        place_res = self.client.post('/api/v1/places/', json={
            "title": "ReviewTest Place",
            "price": 100,
            "latitude": 48.85,
            "longitude": 2.35
        })
        self.place_id = place_res.get_json()["id"]

    def test_get_review_by_id(self):
        res = self.client.post('/api/v1/reviews/', json={
            "text": "Good place.",
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        review_id = res.get_json()["id"]

        get_res = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(get_res.status_code, 200)
        self.assertEqual(get_res.get_json()["text"], "Good place.")

    def test_update_review_valid(self):
        res = self.client.post('/api/v1/reviews/', json={
            "text": "Okay.",
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        review_id = res.get_json()["id"]

        put_res = self.client.put(f'/api/v1/reviews/{review_id}', json={
            "text": "Actually, excellent!",
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(put_res.status_code, 200)
        self.assertEqual(put_res.get_json()["text"], "Actually, excellent!")

if __name__ == '__main__':
    unittest.main()
