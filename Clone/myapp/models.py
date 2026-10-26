from django.conf import settings
from django.db import models


class MediaItem(models.Model):
    MUSIC = "music"
    MOVIE = "movie"
    TYPE_CHOICES = [(MUSIC, "Music"), (MOVIE, "Movie")]

    title = models.CharField(max_length=180)
    creator = models.CharField(max_length=180, blank=True, help_text="Artist for music, director or genre for movies")
    media_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    description = models.TextField(blank=True)
    cover_url = models.URLField(blank=True)
    media_url = models.URLField(blank=True, help_text="Optional playable audio/video URL")
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-featured", "title"]

    def __str__(self):
        return f"{self.title} ({self.get_media_type_display()})"


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=80)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    billing_period = models.CharField(max_length=30, default="month")
    description = models.CharField(max_length=220, blank=True)
    features = models.TextField(blank=True, help_text="One feature per line")
    is_popular = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["price"]

    def __str__(self):
        return f"{self.name} — ₹{self.price}/{self.billing_period}"


class UserSubscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="media_subscriptions")
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT)
    started_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-started_at"]

    def __str__(self):
        return f"{self.user.username}: {self.plan.name}"
