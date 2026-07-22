from django.test import TestCase


class CsrfTests(TestCase):
    def test_returns_csrf_token(self):
        response = self.client.get("/api/csrf")

        self.assertEqual(response.status_code, 200)
        self.assertIn("csrfToken", response.json())
        self.assertIn("csrftoken", response.cookies)
