from django.test import TestCase
from django.urls import reverse
from .models import MediaItem, SubscriptionPlan


class MediaHubTests(TestCase):
    def setUp(self):
        MediaItem.objects.create(title="Test Track", creator="Test Artist", media_type="music", featured=True)
        SubscriptionPlan.objects.create(name="Free", price="0.00", features="Browse")

    def test_home_loads(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_music_search(self):
        response = self.client.get(reverse("music"), {"q": "Test"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Track")

    def test_signup(self):
        response = self.client.post(reverse("signup"), {
            "username": "sampleuser",
            "password1": "Strong-Test-Password-882!",
            "password2": "Strong-Test-Password-882!",
        })
        self.assertEqual(response.status_code, 302)
