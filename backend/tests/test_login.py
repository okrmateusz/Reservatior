import json

from django.contrib.auth import get_user_model
from django.test import TestCase


class LoginTests(TestCase):
    def test_logs_in_with_matching_credentials(self):
        get_user_model().objects.create_user(
            username="user@example.com",
            email="user@example.com",
            password="secret-password",
        )

        response = self.client.post(
            "/api/login",
            data=json.dumps(
                {"email": "User@Example.com", "password": "secret-password"}
            ),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            self.client.session["_auth_user_id"],
            str(get_user_model().objects.get().id),
        )

    def test_rejects_incorrect_password(self):
        get_user_model().objects.create_user(
            username="user@example.com",
            email="user@example.com",
            password="correct-password",
        )

        response = self.client.post(
            "/api/login",
            data=json.dumps(
                {"email": "user@example.com", "password": "incorrect-password"}
            ),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 401)
