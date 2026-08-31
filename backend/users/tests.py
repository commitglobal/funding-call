import json

from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse


class FundingLoginViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse("users-auth:login")
        self.user = get_user_model().objects.create_user(
            email="member@example.com",
            password="correct-password",
        )
        EmailAddress.objects.create(
            user=self.user,
            email=self.user.email,
            primary=True,
            verified=True,
        )

    def test_get_renders_login_page_for_inertia_request(self):
        response = self.client.get(self.login_url, HTTP_X_INERTIA="true")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["component"], "Auth/Login/Index")
        self.assertTrue(response.json()["props"]["class_view"])

    def test_post_with_valid_json_credentials_logs_user_in_and_redirects(self):
        response = self.client.post(
            self.login_url,
            data=json.dumps(
                {
                    "login": self.user.email,
                    "password": "correct-password",
                }
            ),
            content_type="application/json",
        )

        self.assertRedirects(response, reverse("users-profiles:my-profile"))
        self.assertEqual(int(self.client.session["_auth_user_id"]), self.user.pk)

    def test_post_with_invalid_json_credentials_returns_invalid_prop(self):
        response = self.client.post(
            self.login_url,
            data=json.dumps(
                {
                    "login": self.user.email,
                    "password": "wrong-password",
                }
            ),
            content_type="application/json",
            HTTP_X_INERTIA="true",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["component"], "Auth/Login/Index")
        self.assertFalse(response.json()["props"]["valid"])
