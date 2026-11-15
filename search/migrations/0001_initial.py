# Generated for SearchNova initial database schema.
import django.utils.timezone
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="CrawlSeed",
            fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("url", models.URLField(max_length=1000, unique=True)), ("enabled", models.BooleanField(default=True)), ("created_at", models.DateTimeField(auto_now_add=True))],
            options={"ordering": ["url"], "verbose_name": "Crawl seed", "verbose_name_plural": "Crawl seeds"},
        ),
        migrations.CreateModel(
            name="IndexedPage",
            fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("title", models.CharField(blank=True, max_length=300)), ("url", models.URLField(max_length=1000, unique=True)), ("description", models.CharField(blank=True, max_length=500)), ("body_text", models.TextField(blank=True)), ("content_hash", models.CharField(blank=True, db_index=True, max_length=64)), ("status_code", models.PositiveSmallIntegerField(default=200)), ("crawled_at", models.DateTimeField(db_index=True, default=django.utils.timezone.now))],
            options={"ordering": ["-crawled_at"], "indexes": [models.Index(fields=["title"], name="search_title_idx"), models.Index(fields=["crawled_at"], name="search_crawled_idx")]},
        ),
        migrations.CreateModel(
            name="SearchQuery",
            fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("query", models.CharField(max_length=300)), ("results_count", models.PositiveIntegerField(default=0)), ("created_at", models.DateTimeField(auto_now_add=True, db_index=True))],
            options={"ordering": ["-created_at"]},
        ),
    ]
