from django.db import models
from django.utils import timezone


class IndexedPage(models.Model):
    title = models.CharField(max_length=300, blank=True)
    url = models.URLField(max_length=1000, unique=True)
    description = models.CharField(max_length=500, blank=True)
    body_text = models.TextField(blank=True)
    content_hash = models.CharField(max_length=64, blank=True, db_index=True)
    status_code = models.PositiveSmallIntegerField(default=200)
    crawled_at = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        ordering = ["-crawled_at"]
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["crawled_at"]),
        ]

    def __str__(self):
        return self.title or self.url


class CrawlSeed(models.Model):
    url = models.URLField(max_length=1000, unique=True)
    enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["url"]
        verbose_name = "Crawl seed"
        verbose_name_plural = "Crawl seeds"

    def __str__(self):
        return self.url


class SearchQuery(models.Model):
    query = models.CharField(max_length=300)
    results_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.query} ({self.results_count})"


class AIOverviewCache(models.Model):
    query = models.CharField(max_length=300, unique=True, db_index=True)
    overview_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = "AI Overview Cache"
        verbose_name_plural = "AI Overview Caches"

    def __str__(self):
        return self.query