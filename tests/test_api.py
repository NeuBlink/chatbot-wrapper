# File: tests/test_api.py

import unittest
import json
from app import app

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_process_valid_input(self):
        payload = json.dumps({
            "username": "testuser",
            "message_input": "Hello",
            "input_type": "text"
        })
        response = self.app.post('/process', headers={"Content-Type": "application/json"}, data=payload)
        self.assertEqual(response.status_code, 200)

    def test_process_invalid_content_type(self):
        response = self.app.post('/process', data="invalid data")
        self.assertEqual(response.status_code, 400)

    def test_process_missing_fields(self):
        payload = json.dumps({"username": "testuser"})
        response = self.app.post('/process', headers={"Content-Type": "application/json"}, data=payload)
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()