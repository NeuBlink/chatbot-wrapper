# File: locustfile.py

from locust import HttpUser, task, between

class ChatbotUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def ask_question(self):
        self.client.post("/process", json={
            "username": "testuser",
            "message_input": "Hello",
            "input_type": "text"
        })