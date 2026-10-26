from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .models import MediaItem, SubscriptionPlan, UserSubscription


def home(request):
    featured_music = MediaItem.objects.filter(media_type="music", featured=True)[:4]
    featured_movies = MediaItem.objects.filter(media_type="movie", featured=True)[:4]
    plans = SubscriptionPlan.objects.filter(active=True)[:3]
    return render(request, "myapp/home.html", {
        "featured_music": featured_music,
        "featured_movies": featured_movies,
        "plans": plans,
    })


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            next_url = request.GET.get("next") or "home"
            return redirect(next_url)
        messages.error(request, "Username or password is incorrect.")
    return render(request, "myapp/login.html")


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Your account is ready. Welcome to VibeStream!")
        return redirect("home")
    return render(request, "myapp/signup.html", {"form": form})


@require_POST
def logout_view(request):
    logout(request)
    messages.info(request, "You have been signed out.")
    return redirect("home")


def music(request):
    query = request.GET.get("q", "").strip()
    items = MediaItem.objects.filter(media_type="music")
    if query:
        items = items.filter(title__icontains=query) | MediaItem.objects.filter(media_type="music", creator__icontains=query)
    return render(request, "myapp/catalog.html", {"items": items.distinct(), "kind": "music", "query": query})


def movies(request):
    query = request.GET.get("q", "").strip()
    items = MediaItem.objects.filter(media_type="movie")
    if query:
        items = items.filter(title__icontains=query) | MediaItem.objects.filter(media_type="movie", creator__icontains=query)
    return render(request, "myapp/catalog.html", {"items": items.distinct(), "kind": "movies", "query": query})


def plans(request):
    active_subscription = None
    if request.user.is_authenticated:
        active_subscription = UserSubscription.objects.filter(user=request.user, active=True).select_related("plan").first()
    return render(request, "myapp/plans.html", {
        "plans": SubscriptionPlan.objects.filter(active=True),
        "active_subscription": active_subscription,
    })


@login_required
@require_POST
def subscribe(request, plan_id):
    plan = get_object_or_404(SubscriptionPlan, pk=plan_id, active=True)
    UserSubscription.objects.filter(user=request.user, active=True).update(active=False)
    UserSubscription.objects.create(user=request.user, plan=plan, active=True)
    messages.success(request, f"You selected the {plan.name} plan.")
    return redirect("plans")
