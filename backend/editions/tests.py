from django.test import Client, TestCase


class HomepageTest(TestCase):
    def test_homepage_load(self):
        c = Client()
        response = c.get("/")

        self.assertEqual(response.status_code, 200)
