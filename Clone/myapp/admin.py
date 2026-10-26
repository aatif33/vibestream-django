from django.contrib import admin
from .models import MediaItem, SubscriptionPlan, UserSubscription

@admin.register(MediaItem)
class MediaItemAdmin(admin.ModelAdmin):
    list_display = ("title", "media_type", "creator", "featured")
    list_filter = ("media_type", "featured")
    search_fields = ("title", "creator")

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "billing_period", "active", "is_popular")
    list_filter = ("active", "is_popular")

@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ("user", "plan", "started_at", "active")
    list_filter = ("active", "plan")
