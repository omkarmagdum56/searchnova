from django.contrib import admin
from .models import CrawlSeed, IndexedPage, SearchQuery

@admin.register(IndexedPage)
class IndexedPageAdmin(admin.ModelAdmin):
    list_display = ("title", "url", "status_code", "crawled_at")
    search_fields = ("title", "url", "description", "body_text")
    list_filter = ("status_code", "crawled_at")
    readonly_fields = ("crawled_at",)
    list_per_page = 25

@admin.register(CrawlSeed)
class CrawlSeedAdmin(admin.ModelAdmin):
    list_display = ("url", "enabled", "created_at")
    list_filter = ("enabled",)
    search_fields = ("url",)

@admin.register(SearchQuery)
class SearchQueryAdmin(admin.ModelAdmin):
    list_display = ("query", "results_count", "created_at")
    search_fields = ("query",)
    readonly_fields = ("query", "results_count", "created_at")
