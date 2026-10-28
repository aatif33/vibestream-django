from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from myapp import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("logout/", views.logout_view, name="logout"),
    path("music/", views.music, name="music"),
    path("movies/", views.movies, name="movies"),
    path("plans/", views.plans, name="plans"),
    path("subscribe/<int:plan_id>/", views.subscribe, name="subscribe"),
    path("error-codes/", views.error_codes, name="error_codes"),
    path("faq/", views.faq, name="faq"),
    path("assistant/", views.assistant, name="assistant"),
    path("assistant/ask/", views.assistant_ask, name="assistant_ask"),
    path("feedback/", views.feedback_page, name="feedback"),
    path("feedback/submit/", views.feedback_submit, name="feedback_submit"),
    path("monitoring/", views.monitoring, name="monitoring"),
    path("health/", views.health, name="health"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
