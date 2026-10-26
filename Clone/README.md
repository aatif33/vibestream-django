# VibeStream — Django starter

A polished Django starter for a combined music and movie discovery app. The current project was extended rather than replaced.

## Features
- Django authentication: sign up, log in, log out
- Music and movie catalogs stored in the database
- Search by title or artist/director field
- Separate `static/css/music.css` and `static/css/movie.css`
- Shared styling and JavaScript kept in their own folders
- Subscription plan management and user plan selection (demo only)
- Django admin for managing media, plans, and subscriptions
- SQLite database for local development

## Run on Windows

Open a terminal in the folder containing `manage.py`:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install "Django>=5.2,<5.3"
python manage.py makemigrations myapp
python manage.py migrate
python manage.py seed_demo
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/

If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in that terminal and activate again.

## Admin
Visit http://127.0.0.1:8000/admin/ and sign in with the superuser you created. Add/edit media and plans there. Cover URL should be a direct image URL; media URL should be a direct playable audio URL or a link to the movie content.

## Structure

```text
MediaHub_Django/
├── app/                 # Django project settings and root URLs
├── myapp/               # views, models, admin, migrations
│   └── templates/myapp/ # Django HTML templates
├── static/
│   ├── css/
│   │   ├── main.css     # shared layout, login, signup, plans
│   │   ├── music.css    # music-specific theme
│   │   └── movie.css    # movie-specific theme
│   └── js/main.js       # password toggles, audio controls, notices
├── manage.py
└── README.md
```

## Notes
- The subscription form records a selected plan in SQLite; it does **not** charge a card. Add a payment provider and webhook verification before accepting real payments.
- Audio playback requires a direct URL to an audio file supported by the browser. Movie playback is represented as an external link in this starter.
- The CSS imports Google Fonts; a network connection is needed for those fonts, but the interface falls back to local system fonts.
- `DEBUG=True` and the development secret key are for local development only. Change both before deploying.
