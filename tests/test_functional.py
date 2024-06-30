# File: tests/test_functional.py

import unittest
import json
import os
from pymongo import MongoClient
from app import app
from config import get_db_creds

class TestFunctional(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Get the MongoDB credentials
        cls.mongodb_uri, cls.db_name = get_db_creds()
        
        # Connect to MongoDB
        cls.client = MongoClient(cls.mongodb_uri)
        cls.db = cls.client[cls.db_name]
        
        # Use the same collection as the main application
        cls.users_collection = cls.db['users']
        
        # Set up the Flask test client
        cls.app = app.test_client()
        
    @classmethod
    def tearDownClass(cls):
        # Close the MongoDB connection
        cls.client.close()

    def setUp(self):
        # Clear the users collection before each test
        self.users_collection.delete_many({})

    def test_process_new_user(self):
        payload = json.dumps({
            "username": "new_test_user",
            "message_input": "Hello, this is a test message.",
            "input_type": "text"
        })
        response = self.app.post('/process', 
                                 headers={"Content-Type": "application/json"}, 
                                 data=payload)
        
        self.assertEqual(response.status_code, 200)
        
        # Check if the user was created in the database
        user = self.users_collection.find_one({"user_id": "new_test_user"})
        self.assertIsNotNone(user, "User was not created in the database")

    def test_process_existing_user(self):
        # Create a user first
        self.users_collection.insert_one({"user_id": "existing_test_user"})
        
        payload = json.dumps({
            "username": "existing_test_user",
            "message_input": "Hello again, this is another test message.",
            "input_type": "text"
        })
        response = self.app.post('/process', 
                                 headers={"Content-Type": "application/json"}, 
                                 data=payload)
        
        self.assertEqual(response.status_code, 200)

    def test_process_invalid_input(self):
        payload = json.dumps({
            "username": "test_user",
            "message_input": "Invalid message",
            "input_type": "invalid_type"
        })
        response = self.app.post('/process', 
                                 headers={"Content-Type": "application/json"}, 
                                 data=payload)
        
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()