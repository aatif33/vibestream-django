
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
]

# Serve local music, movie, and image files during development
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
