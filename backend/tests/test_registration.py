import json

from django.contrib.auth import get_user_model
from django.test import Client, TestCase


class RegistrationTests(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        csrf_response = self.client.get("/api/csrf")
        self.csrf_token = csrf_response.json()["csrfToken"]

    def register(self, email, password, password_confirmation):
        return self.client.post(
            "/api/register",
            data=json.dumps(
                {
                    "email": email,
                    "password": password,
                    "passwordConfirmation": password_confirmation,
                }
            ),
            content_type="application/json",
            headers={
                "origin": "http://testserver",
                "x-csrftoken": self.csrf_token,
            },
        )

    def test_registers_user(self):
        response = self.register(
            "User@Example.com",
            "Horses-Quartz-47!",
            "Horses-Quartz-47!",
        )

        self.assertEqual(response.status_code, 201)
        user = get_user_model().objects.get(username="user@example.com")
        self.assertTrue(user.check_password("Horses-Quartz-47!"))

    def test_rejects_different_passwords(self):
        response = self.register(
            "user@example.com",
            "Horses-Quartz-47!",
            "different-password",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"error": "Hasła nie są takie same."})
        self.assertFalse(get_user_model().objects.exists())

    def test_rejects_empty_email(self):
        response = self.register("", "Horses-Quartz-47!", "Horses-Quartz-47!")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"error": "Podaj poprawny adres e-mail."})
        self.assertFalse(get_user_model().objects.exists())

    def test_rejects_invalid_email(self):
        response = self.register(
            "invalid-email",
            "Horses-Quartz-47!",
            "Horses-Quartz-47!",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"error": "Podaj poprawny adres e-mail."})
        self.assertFalse(get_user_model().objects.exists())

    def test_rejects_weak_password(self):
        response = self.register("user@example.com", "password", "password")

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
        self.assertFalse(get_user_model().objects.exists())
