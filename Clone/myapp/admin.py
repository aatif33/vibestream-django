from django.contrib import admin
from .models import AIQueryLog, AppEvent, ErrorCode, FAQ, Feedback, MediaItem, SubscriptionPlan, UserSubscription

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

@admin.register(ErrorCode)
class ErrorCodeAdmin(admin.ModelAdmin):
    list_display = ("code", "title", "category", "severity", "active", "updated_at")
    list_filter = ("severity", "category", "active")
    search_fields = ("code", "title", "description", "possible_causes")

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "category", "active", "sort_order")
    list_filter = ("category", "active")
    search_fields = ("question", "answer")

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("feedback_type", "rating", "reviewed", "created_at", "user")
    list_filter = ("feedback_type", "rating", "reviewed")
    search_fields = ("message",)
    readonly_fields = ("created_at",)

@admin.register(AppEvent)
class AppEventAdmin(admin.ModelAdmin):
    list_display = ("created_at", "level", "event_type", "status_code", "path")
    list_filter = ("level", "event_type", "created_at")
    search_fields = ("message", "path", "event_type")
    readonly_fields = tuple(f.name for f in AppEvent._meta.fields)

@admin.register(AIQueryLog)
class AIQueryLogAdmin(admin.ModelAdmin):
    list_display = ("created_at", "success", "latency_ms", "user")
    list_filter = ("success", "created_at")
    search_fields = ("question", "answer_preview")
    readonly_fields = tuple(f.name for f in AIQueryLog._meta.fields)
