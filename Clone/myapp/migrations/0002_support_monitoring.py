import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]
    operations = [
        migrations.CreateModel(name="ErrorCode", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("code", models.CharField(max_length=30, unique=True)), ("title", models.CharField(max_length=140)),
            ("category", models.CharField(default="General", max_length=80)),
            ("severity", models.CharField(choices=[("info", "Info"), ("low", "Low"), ("medium", "Medium"), ("high", "High"), ("critical", "Critical")], default="medium", max_length=10)),
            ("description", models.TextField()), ("possible_causes", models.TextField(blank=True)),
            ("resolution_steps", models.TextField()), ("prevention", models.TextField(blank=True)),
            ("active", models.BooleanField(default=True)), ("updated_at", models.DateTimeField(auto_now=True)),
        ], options={"ordering": ["severity", "code"]}),
        migrations.CreateModel(name="FAQ", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("category", models.CharField(default="General", max_length=80)), ("question", models.CharField(max_length=240)),
            ("answer", models.TextField()), ("active", models.BooleanField(default=True)), ("sort_order", models.PositiveIntegerField(default=0)),
        ], options={"ordering": ["sort_order", "question"], "verbose_name": "FAQ entry", "verbose_name_plural": "FAQ entries"}),
        migrations.CreateModel(name="Feedback", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("feedback_type", models.CharField(choices=[("bug", "Bug report"), ("idea", "Feature idea"), ("experience", "General feedback")], default="experience", max_length=12)),
            ("rating", models.PositiveSmallIntegerField(default=5)), ("message", models.TextField(max_length=2000)),
            ("page", models.CharField(blank=True, max_length=200)), ("created_at", models.DateTimeField(auto_now_add=True)),
            ("reviewed", models.BooleanField(default=False)),
            ("user", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
        ], options={"ordering": ["-created_at"]}),
        migrations.CreateModel(name="AppEvent", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("event_type", models.CharField(db_index=True, max_length=80)),
            ("level", models.CharField(choices=[("info", "Info"), ("warning", "Warning"), ("error", "Error")], default="info", max_length=10)),
            ("message", models.CharField(max_length=500)), ("path", models.CharField(blank=True, max_length=300)),
            ("status_code", models.PositiveSmallIntegerField(blank=True, null=True)), ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
            ("user", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
        ], options={"ordering": ["-created_at"]}),
        migrations.CreateModel(name="AIQueryLog", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("question", models.CharField(max_length=1000)), ("answer_preview", models.CharField(blank=True, max_length=500)),
            ("success", models.BooleanField(default=False)), ("latency_ms", models.PositiveIntegerField(default=0)),
            ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
            ("user", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
        ], options={"ordering": ["-created_at"]}),
    ]
