import re
from django.db.models import Q
from .models import IndexedPage

STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from",
    "in", "is", "it", "of", "on", "or", "the", "to", "with", "what",
    "how", "where", "when", "who", "why", "this", "that", "about",
}

def tokenize(query):
    words = re.findall(r"[a-zA-Z0-9][a-zA-Z0-9+#.-]*", query.lower())
    return list(dict.fromkeys(w for w in words if w not in STOP_WORDS))[:12]

def search_pages(query, limit=50):
    terms = tokenize(query)
    if not terms:
        return []
    condition = Q()
    for term in terms:
        condition |= Q(title__icontains=term) | Q(description__icontains=term) | Q(body_text__icontains=term)
    candidates = IndexedPage.objects.filter(condition).distinct().only(
        "id", "title", "url", "description", "body_text", "crawled_at"
    )[:500]
    scored = []
    phrase = query.strip().lower()
    for page in candidates:
        title = (page.title or "").lower()
        description = (page.description or "").lower()
        body = (page.body_text or "").lower()
        score = 0.0
        matched = 0
        for term in terms:
            occurrences = title.count(term) + description.count(term) + body.count(term)
            if occurrences:
                matched += 1
            score += title.count(term) * 10 + description.count(term) * 5 + body.count(term)
        if phrase and phrase in title:
            score += 18
        elif phrase and phrase in description:
            score += 8
        # Prefer pages matching more of the user's keywords over a single repeated word.
        score += matched * 3
        if score:
            scored.append((score, page))
    scored.sort(key=lambda item: (item[0], item[1].crawled_at), reverse=True)
    return [{"page": page, "score": round(score, 2)} for score, page in scored[:limit]]
