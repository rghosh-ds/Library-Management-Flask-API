import unittest
from flask import Flask
from flask.testing import FlaskClient
from flask_jwt_extended import create_access_token
from library_management_app import create_app, db
from library_management_app.models import Book, Member
import time


class RoutesTestCase(unittest.TestCase):
    app: Flask
    client: FlaskClient

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app.config['TESTING'] = True
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        cls.client = cls.app.test_client()

        with cls.app.app_context():
            db.create_all()

    def setUp(self):
        with self.app.app_context():
            db.session.query(Book).delete()
            db.session.query(Member).delete()
            db.session.commit()

        self.client.post('/register', json={"username": "testuser", "password": "testpassword"})
        response = self.client.post('/login', json={"username": "testuser", "password": "testpassword"})
        self.access_token = response.json['access_token']

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_healthcheck(self):
        response = self.client.get('/healthcheck')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Server is running"})

    def test_register(self):
        unique_username = f"user_{int(time.time())}"  # Create a unique username
        response = self.client.post('/register', json={"username": unique_username, "password": "testpassword"})
        self.assertEqual(response.status_code, 201)
        self.assertIn("Member registered successfully", response.json['message'])

    def test_login(self):
        payload = {"username": "test_user", "password": "password123"}
        self.client.post('/register', json=payload)

        response = self.client.post('/login', json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.json)

        response = self.client.post('/login', json={"username": "test_user", "password": "wrong_password"})
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json, {"message": "Invalid credentials"})


    def test_add_and_get_books(self):
        self.client.post('/books', json={"title": "Book Title", "author": "Author Name"},
                         headers={"Authorization": f"Bearer {self.access_token}"})

        response = self.client.get('/books?page=1&per_page=1',
                                    headers={"Authorization": f"Bearer {self.access_token}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json['books']), 1)
        self.assertEqual(response.json['books'][0]['title'], "Book Title")


if __name__ == "__main__":
    unittest.main()
