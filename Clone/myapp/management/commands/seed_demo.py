from django.core.management.base import BaseCommand
from myapp.models import MediaItem, SubscriptionPlan


class Command(BaseCommand):
    help = "Add sample music, movie, and subscription plan records."

    def handle(self, *args, **options):
        media = [
            {"title": "Midnight City", "creator": "M83", "media_type": "music", "description": "A late-night electronic anthem.", "featured": True},
            {"title": "Golden Hour", "creator": "JVKE", "media_type": "music", "description": "A warm pop track for slow afternoons.", "featured": True},
            {"title": "Ocean Eyes", "creator": "Billie Eilish", "media_type": "music", "description": "Dreamy vocals and a soft atmosphere.", "featured": True},
            {"title": "Electric Feel", "creator": "MGMT", "media_type": "music", "description": "Indie-electronic energy.", "featured": True},
            {"title": "After Hours", "creator": "Drama · 2024", "media_type": "movie", "description": "A city night changes everything.", "featured": True},
            {"title": "The Last Horizon", "creator": "Adventure · 2023", "media_type": "movie", "description": "A journey beyond the familiar.", "featured": True},
            {"title": "Paper Skies", "creator": "Romance · 2025", "media_type": "movie", "description": "Two lives meet at the right moment.", "featured": True},
            {"title": "Echoes", "creator": "Mystery · 2024", "media_type": "movie", "description": "Every answer opens another question.", "featured": True},
        ]
        for item in media:
            MediaItem.objects.update_or_create(title=item["title"], media_type=item["media_type"], defaults=item)
        plans = [
            {"name": "Free", "price": "0.00", "billing_period": "month", "description": "A little taste of everything.", "features": "Browse music and movies\nDiscover featured picks\nStandard experience"},
            {"name": "Plus", "price": "149.00", "billing_period": "month", "description": "More room for your favorites.", "features": "Everything in Free\nAd-free experience (demo)\nPersonalized picks\nHigh-quality listening", "is_popular": True},
            {"name": "Ultimate", "price": "299.00", "billing_period": "month", "description": "The full VibeStream experience.", "features": "Everything in Plus\nPremium collection access (demo)\nEarly access to new features\nSupport the creators"},
        ]
        for plan in plans:
            SubscriptionPlan.objects.update_or_create(name=plan["name"], defaults=plan)
        self.stdout.write(self.style.SUCCESS("Demo media and subscription plans are ready."))
