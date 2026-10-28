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
    media_url = models.URLField(blank=True, help_text="Use a direct, playable audio/video URL from persistent storage")
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


class ErrorCode(models.Model):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    SEVERITY_CHOICES = [(v, v.title()) for v in (INFO, LOW, MEDIUM, HIGH, CRITICAL)]
    code = models.CharField(max_length=30, unique=True)
    title = models.CharField(max_length=140)
    category = models.CharField(max_length=80, default="General")
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default=MEDIUM)
    description = models.TextField()
    possible_causes = models.TextField(blank=True, help_text="One cause per line")
    resolution_steps = models.TextField(help_text="One step per line")
    prevention = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["severity", "code"]

    def __str__(self):
        return f"{self.code} — {self.title}"


class FAQ(models.Model):
    category = models.CharField(max_length=80, default="General")
    question = models.CharField(max_length=240)
    answer = models.TextField()
    active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "question"]
        verbose_name = "FAQ entry"
        verbose_name_plural = "FAQ entries"

    def __str__(self):
        return self.question


class Feedback(models.Model):
    BUG = "bug"
    IDEA = "idea"
    EXPERIENCE = "experience"
    TYPE_CHOICES = [(BUG, "Bug report"), (IDEA, "Feature idea"), (EXPERIENCE, "General feedback")]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    feedback_type = models.CharField(max_length=12, choices=TYPE_CHOICES, default=EXPERIENCE)
    rating = models.PositiveSmallIntegerField(default=5)
    message = models.TextField(max_length=2000)
    page = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_feedback_type_display()} ({self.rating}/5) — {self.created_at:%Y-%m-%d}"


class AppEvent(models.Model):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    LEVEL_CHOICES = [(INFO, "Info"), (WARNING, "Warning"), (ERROR, "Error")]
    event_type = models.CharField(max_length=80, db_index=True)
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, default=INFO)
    message = models.CharField(max_length=500)
    path = models.CharField(max_length=300, blank=True)
    status_code = models.PositiveSmallIntegerField(null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.level.upper()} {self.event_type}: {self.message[:80]}"


class AIQueryLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    question = models.CharField(max_length=1000)
    answer_preview = models.CharField(max_length=500, blank=True)
    success = models.BooleanField(default=False)
    latency_ms = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"AI query ({'ok' if self.success else 'failed'}) at {self.created_at:%Y-%m-%d %H:%M}"
