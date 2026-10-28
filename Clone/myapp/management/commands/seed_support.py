from django.core.management.base import BaseCommand
from myapp.models import ErrorCode, FAQ

class Command(BaseCommand):
    help = "Create starter FAQ and troubleshooting entries for VibeStream"
    def handle(self, *args, **options):
        faqs = [
            ("Playback", "Why won't a song play?", "Check that the track has a direct, publicly accessible audio URL (for example an MP3 or supported stream). A local /media/ path on a serverless deployment may not be available. Try the URL directly in a new browser tab."),
            ("Account", "How do I create an account?", "Use Get started to create an account with a unique username and a strong password. Keep your credentials private."),
            ("Plans", "Does selecting a plan charge me?", "No. The current project records your selected demo plan only; it does not collect payment details or charge a payment method."),
            ("Privacy", "How is my feedback used?", "Feedback is stored for the project team to review. Do not include passwords, payment details, API keys or other secrets."),
            ("AI assistant", "Why might the AI assistant be unavailable?", "The assistant requires OPENAI_API_KEY to be configured on the server. If the provider is unavailable, use the FAQ and error-code library."),
        ]
        for category, question, answer in faqs:
            FAQ.objects.get_or_create(question=question, defaults={"category": category, "answer": answer})
        errors = [
            ("VS-PLAY-001", "Audio URL unavailable", "Playback", "medium", "The browser cannot retrieve the audio URL.", "The file is local to a deployment; the URL is misspelled; storage permissions block access.", "Open the audio URL directly; confirm it returns an audio file; replace local media paths with a persistent storage URL.", "Use persistent object storage and verify URLs before publishing tracks."),
            ("VS-AUTH-001", "Sign-in failed", "Account", "low", "The username and password were not accepted.", "Incorrect credentials; account does not exist.", "Check the username; use the password reset process if available; contact an administrator if the issue persists.", "Use a unique password and never share account credentials."),
            ("VS-DB-001", "Database unavailable", "Backend", "high", "The application could not read or write persistent database data.", "Database URL is missing or invalid; hosted database is unreachable; migrations have not been applied.", "Check DATABASE_URL in deployment environment variables; verify the database provider status; apply Django migrations against the hosted database.", "Use hosted PostgreSQL in production and test database connectivity with the health endpoint."),
            ("VS-AI-001", "AI assistant unavailable", "AI assistant", "medium", "The assistant could not get a response from its AI provider.", "OPENAI_API_KEY is missing; network timeout; provider quota or rate limit.", "Confirm OPENAI_API_KEY is set on the server; check provider status and usage limits; retry later or use FAQ search.", "Keep API keys server-side and implement rate limits and a fallback path."),
            ("VS-SEC-001", "Request rejected by security checks", "Security", "medium", "A request was rejected by host validation or CSRF protection.", "Host not listed in ALLOWED_HOSTS; trusted origin mismatch; missing CSRF token.", "Check the exact deployment hostname; configure CSRF_TRUSTED_ORIGINS with HTTPS origins; submit forms with the Django CSRF token.", "Keep production host and CSRF settings aligned with the deployed domain."),
        ]
        for code, title, category, severity, description, causes, steps, prevention in errors:
            ErrorCode.objects.get_or_create(code=code, defaults={"title": title, "category": category, "severity": severity, "description": description, "possible_causes": causes, "resolution_steps": steps, "prevention": prevention})
        self.stdout.write(self.style.SUCCESS("Starter FAQ and error-code entries are ready."))
