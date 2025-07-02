import unittest
import uuid
from app import create_app

class TestUser(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

        # on fait login admin pour obtenir le JWT
        login_res = self.client.post('/api/v1/auth/login', json={
            "email": "admin@example.com",
            "password": "adminpassword"
        })
        self.assertEqual(login_res.status_code, 200)
        self.token = login_res.get_json()["access_token"]
        self.headers = {"Authorization": f"Bearer {self.token}"}

    def test_get_user_by_id(self):
        # créer user
        post_res = self.client.post('/api/v1/users/', json={
            "first_name": "Léo",
            "last_name": "Salin",
            "email": "leo.salins@example.com",
            "password": "securepass"
        }, headers=self.headers)
        self.assertEqual(post_res.status_code, 201)
        user_id = post_res.get_json()["id"]

        # récupérer user par ID
        get_res = self.client.get(f'/api/v1/users/{user_id}', headers=self.headers)
        self.assertEqual(get_res.status_code, 200)
        self.assertEqual(get_res.get_json()["email"], "leo.salins@example.com")

    def test_update_user_valid(self):
        post_res = self.client.post('/api/v1/users/', json={
            "first_name": "Anna",
            "last_name": "Dupont",
            "email": f"anna-{uuid.uuid4()}@example.com",
            "password": "pass"
        }, headers=self.headers)
        user_id = post_res.get_json()["id"]

        put_res = self.client.put(f'/api/v1/users/{user_id}', json={
            "first_name": "Anna-Marie",
            "last_name": "Dupont",
            "email": f"anna-marie-{uuid.uuid4()}@example.com",
            "password": "newpass"
        }, headers=self.headers)
        self.assertEqual(put_res.status_code, 200)
        self.assertEqual(put_res.get_json()["first_name"], "Anna-Marie")

if __name__ == '__main__':
    unittest.main()
