# VibeStream — full-stack Django media and support platform

VibeStream combines music/movie discovery and demo subscription selection with a searchable FAQ, structured error-code library, API-backed AI support assistant, feedback capture, and staff-only monitoring.

## Features
- Django signup/login/logout and admin
- Music/movie catalogs and demo plan selection
- Searchable error-code library with severity, causes, resolution and prevention
- FAQ search
- AI assistant using OpenAI Chat Completions API (`OPENAI_API_KEY`); retrieves relevant FAQ/error-code context and shows reference labels
- Assistant fallback when no API key is configured or provider fails
- Feedback form stored in the database
- Staff-only monitoring dashboard for events, feedback and AI query latency/outcomes
- `/health/` endpoint checks database connectivity
- Environment-based secrets, secure production cookies, host/CSRF configuration
- PostgreSQL support via `DATABASE_URL`; SQLite remains for local development

## Windows local setup
Run from the folder containing `manage.py` (the `Clone` directory):

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py seed_support
python manage.py createsuperuser
$env:DJANGO_DEBUG = "True"
python manage.py runserver
```

Open `http://127.0.0.1:8000/`. Admin: `http://127.0.0.1:8000/admin/`.

## Environment variables
Set these in the host's environment-variable settings; do not commit real values:

- `DJANGO_SECRET_KEY`: new random secret key
- `DJANGO_DEBUG`: `False` in production
- `DJANGO_ALLOWED_HOSTS`: comma-separated hostnames, e.g. `vibestream-django.vercel.app,.vercel.app`
- `CSRF_TRUSTED_ORIGINS`: comma-separated full origins, e.g. `https://vibestream-django.vercel.app,https://*.vercel.app`
- `DATABASE_URL`: PostgreSQL connection URL for persistent production storage. If absent, local SQLite is used; do not rely on SQLite persistence on Vercel.
- `OPENAI_API_KEY`: server-side AI provider key
- `OPENAI_MODEL`: optional, defaults to `gpt-4o-mini`

After setting a hosted database URL, run `python manage.py migrate` against that database and `python manage.py seed_support`. Do not assume migrations are automatically applied by deployment. Use a private terminal/environment for the connection string; never paste it into chat or source control.

## Pages
- `/` home
- `/music/`, `/movies/`, `/plans/`
- `/error-codes/`, `/faq/`, `/assistant/`, `/feedback/`
- `/monitoring/` (staff users only)
- `/health/` (database health check)
- `/admin/`

## Important limitations and security notes
- Plan selection is a demonstration only; it does not process payments.
- For reliable production login, subscriptions and feedback, use hosted PostgreSQL rather than Vercel's ephemeral/read-only filesystem.
- Audio/video should use direct playable URLs from persistent object storage or an authorized media provider; local `media/` files are for development only.
- Never expose `OPENAI_API_KEY`, `DATABASE_URL`, or `DJANGO_SECRET_KEY` to frontend JavaScript or GitHub.
- The assistant uses the OpenAI API only when `OPENAI_API_KEY` is configured. It should not be described as available until tested with a valid key.
- Monitoring stores limited event metadata and AI question/answer previews. Avoid asking users for sensitive personal data and review retention before public production use.
