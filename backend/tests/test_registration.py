import json

from django.contrib.auth import get_user_model
from django.test import Client, TestCase


class RegistrationTests(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        csrf_response = self.client.get("/api/csrf")
        self.csrf_token = csrf_response.json()["csrfToken"]

    def register(
        self,
        email,
        password,
        password_confirmation,
        first_name="Jan",
        last_name="Kowalski",
    ):
        return self.client.post(
            "/api/register",
            data=json.dumps(
                {
                    "firstName": first_name,
                    "lastName": last_name,
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
        self.assertEqual(user.first_name, "Jan")
        self.assertEqual(user.last_name, "Kowalski")

    def test_rejects_missing_first_or_last_name(self):
        for first_name, last_name in (("", "Kowalski"), ("Jan", "")):
            with self.subTest(first_name=first_name, last_name=last_name):
                response = self.register(
                    "user@example.com",
                    "Horses-Quartz-47!",
                    "Horses-Quartz-47!",
                    first_name=first_name,
                    last_name=last_name,
                )

                self.assertEqual(response.status_code, 400)
                self.assertEqual(
                    response.json(),
                    {"error": "Podaj imię i nazwisko."},
                )
                self.assertFalse(get_user_model().objects.exists())

    def test_rejects_name_longer_than_database_field(self):
        response = self.register(
            "user@example.com",
            "Horses-Quartz-47!",
            "Horses-Quartz-47!",
            first_name="a" * 151,
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"error": "Imię i nazwisko mogą mieć maksymalnie 150 znaków."},
        )
        self.assertFalse(get_user_model().objects.exists())

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
