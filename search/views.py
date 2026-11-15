import requests
import logging

from django.shortcuts import render
from django.db.models import Count
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.utils import timezone
from django.contrib.admin.views.decorators import staff_member_required

from datetime import timedelta

from .models import (
    CrawlSeed,
    IndexedPage,
    SearchQuery,
    AIOverviewCache
)

from .searching import search_pages
from .services import search_duckduckgo


# =====================================================
# LOGGER
# =====================================================

logger = logging.getLogger(__name__)


# =====================================================
# HELPER: GET TITLE AND CONTENT FROM ANY RESULT
# =====================================================

def get_item_data(item):
    title = ""
    body = ""

    if isinstance(item, dict):
        page = item.get("page")
        if isinstance(page, dict):
            page_title = page.get("title", "")
            page_body = (
                page.get("body_text", "")
                or page.get("content", "")
                or page.get("description", "")
            )
        elif page is not None:
            page_title = getattr(page, "title", "")
            page_body = (
                getattr(page, "body_text", "")
                or getattr(page, "content", "")
                or getattr(page, "description", "")
            )
        else:
            page_title = ""
            page_body = ""

        title = item.get("title") or page_title or ""
        body = (
            item.get("body")
            or item.get("body_text")
            or item.get("content")
            or item.get("description")
            or page_body
            or ""
        )
    else:
        title = getattr(item, "title", "") or ""
        body = (
            getattr(item, "body_text", "")
            or getattr(item, "content", "")
            or getattr(item, "body", "")
            or getattr(item, "description", "")
            or ""
        )

    return str(title), str(body)


# =====================================================
# HELPER: CATEGORY FILTER
# =====================================================

def filter_category(items, category):
    if category not in ["all", "tech", "news"]:
        category = "all"

    if category == "all":
        return items

    filtered_items = []

    tech_keywords = [
        "tech", "technology", "python", "django",
        "html", "css", "javascript", "software",
        "programming", "computer", "coding",
        "database", "developer", "artificial intelligence"
    ]

    news_keywords = [
        "news", "update", "latest", "today",
        "breaking", "announcement", "report", "current affairs"
    ]

    keywords = tech_keywords if category == "tech" else news_keywords

    for item in items:
        title, body = get_item_data(item)
        combined_text = (title + " " + body).lower()
        if any(word in combined_text for word in keywords):
            filtered_items.append(item)

    return filtered_items


# =====================================================
# HELPER: LOCAL OLLAMA AI OVERVIEW
# =====================================================

def generate_ai_overview(query, items):
    clean_query = query.strip().lower()
    if not clean_query:
        return None

    # STEP 1: CHECK DATABASE CACHE
    try:
        cached_obj = AIOverviewCache.objects.filter(query=clean_query).first()
        if cached_obj and cached_obj.overview_text:
            logger.info("AI Overview Cache Hit: %s", clean_query)
            return cached_obj.overview_text
    except Exception:
        logger.exception("AI Overview Cache Read Failed.")

    try:
        # STEP 2: COLLECT SEARCH RESULTS
        context_texts = []
        for item in items[:3]:
            title, body = get_item_data(item)
            if title or body:
                context_texts.append(f"Title: {title}\nContent: {body[:700]}")

        context_text = "\n\n".join(context_texts)
        if not context_text:
            return None

        # STEP 3: CREATE AI PROMPT
        ai_prompt = f"""
You are SearchNova AI, an intelligent search assistant.

User Search Query:
{query}

Available Search Results:
<context>
{context_text}
</context>

Instructions:
1. Answer the user's query clearly.
2. Use the provided search results as reference.
3. Do not invent facts.
4. If the provided information is insufficient, mention that.
5. Keep the answer concise and easy to understand using simple paragraphs and bullet points.
"""

        # STEP 4: CONNECT TO LOCAL OLLAMA SERVER
        ollama_url = "http://127.0.0.1:11434/api/generate"
        payload = {
            "model": "llama3.2",
            "prompt": ai_prompt,
            "stream": False
        }

        response = requests.post(ollama_url, json=payload, timeout=(5, 60))
        response.raise_for_status()

        res_data = response.json()
        answer = res_data.get("response", "").strip()

        if not answer:
            return None

        # STEP 5: SAVE RESPONSE IN DATABASE
        AIOverviewCache.objects.update_or_create(
            query=clean_query,
            defaults={"overview_text": answer}
        )

        return answer

    except Exception:
        logger.exception("Ollama Local AI generation failed.")
        return None


# =====================================================
# HOME PAGE
# =====================================================

def home(request):
    context = {
        "indexed_count": IndexedPage.objects.count(),
        "seed_count": CrawlSeed.objects.filter(enabled=True).count(),
        "has_index": IndexedPage.objects.exists(),
        "recent_queries": (
            SearchQuery.objects
            .values("query")
            .annotate(total=Count("id"))
            .order_by("-total", "query")[:5]
        ),
    }
    return render(request, "search/home.html", context)


# =====================================================
# SEARCH RESULTS PAGE
# =====================================================

def results(request):
    query = request.GET.get("q", "").strip()[:300]
    category = request.GET.get("category", "all").strip().lower()

    if category not in ["all", "tech", "news"]:
        category = "all"

    items = []
    source_type = "Local Database"
    ai_overview = None

    if query:
        # STEP 1: LOCAL DATABASE SEARCH
        try:
            local_items = search_pages(query)
            local_items = [] if local_items is None else list(local_items)
        except Exception:
            local_items = []

        # STEP 2: CATEGORY FILTERING
        filtered_local = filter_category(local_items, category)

        # STEP 3: LIVE WEB SEARCH FALLBACK
        if filtered_local:
            items = filtered_local
            source_type = "SearchNova Index"
        else:
            try:
                api_results = search_duckduckgo(query)
                api_results = [] if api_results is None else list(api_results)
                items = filter_category(api_results, category)
                source_type = "Live Web Results"
            except Exception:
                items = []
                source_type = "Search Error"

        # STEP 4: OLLAMA AI OVERVIEW
        if items:
            ai_overview = generate_ai_overview(query, items)

        # STEP 5: SAVE SEARCH HISTORY
        try:
            SearchQuery.objects.create(query=query, results_count=len(items))
        except Exception:
            pass

    # PAGINATION
    paginator = Paginator(items, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "query": query,
        "items": page_obj,
        "page_obj": page_obj,
        "result_count": len(items),
        "indexed_count": IndexedPage.objects.count(),
        "source_type": source_type,
        "current_category": category,
        "ai_overview": ai_overview,
    }
    return render(request, "search/results.html", context)


# =====================================================
# SEARCH AUTO-COMPLETE SUGGESTIONS API
# =====================================================

def search_suggestions(request):
    query = request.GET.get("q", "").strip()[:100]
    suggestions = []

    if query and len(query) >= 2:
        history_matches = (
            SearchQuery.objects
            .filter(query__icontains=query)
            .values_list("query", flat=True)
            .distinct()[:5]
        )
        title_matches = (
            IndexedPage.objects
            .filter(title__icontains=query)
            .values_list("title", flat=True)
            .distinct()[:5]
        )

        combined = list(history_matches) + list(title_matches)
        seen = set()

        for item in combined:
            item_clean = item.strip()
            if not item_clean:
                continue
            item_lower = item_clean.lower()
            if item_lower not in seen:
                seen.add(item_lower)
                suggestions.append(item_clean)
            if len(suggestions) >= 6:
                break

    return JsonResponse({"suggestions": suggestions})


# =====================================================
# STAFF ANALYTICS DASHBOARD
# =====================================================

@staff_member_required(login_url="/admin/login/")
def analytics_dashboard(request):
    today = timezone.localdate()

    total_searches = SearchQuery.objects.count()
    today_searches = SearchQuery.objects.filter(created_at__date=today).count()
    unique_queries = SearchQuery.objects.values("query").distinct().count()
    no_result_searches = SearchQuery.objects.filter(results_count=0).count()

    top_queries = (
        SearchQuery.objects
        .values("query")
        .annotate(total=Count("id"))
        .order_by("-total", "query")[:10]
    )

    recent_searches = SearchQuery.objects.order_by("-created_at")[:10]

    daily_labels = []
    daily_counts = []

    for offset in range(6, -1, -1):
        day = today - timedelta(days=offset)
        daily_labels.append(day.strftime("%a"))
        daily_counts.append(SearchQuery.objects.filter(created_at__date=day).count())

    max_daily_count = max(daily_counts, default=0)
    daily_stats = [
        {
            "label": label,
            "count": count,
            "percentage": round((count / max_daily_count) * 100) if max_daily_count else 0,
        }
        for label, count in zip(daily_labels, daily_counts)
    ]

    context = {
        "total_searches": total_searches,
        "today_searches": today_searches,
        "unique_queries": unique_queries,
        "no_result_searches": no_result_searches,
        "top_queries": top_queries,
        "recent_searches": recent_searches,
        "daily_labels": daily_labels,
        "daily_counts": daily_counts,
        "daily_stats": daily_stats,
        "indexed_count": IndexedPage.objects.count(),
        "seed_count": CrawlSeed.objects.filter(enabled=True).count(),
    }
    return render(request, "search/analytics.html", context)