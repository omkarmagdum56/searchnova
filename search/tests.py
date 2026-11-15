from django.test import TestCase
from django.urls import reverse
from .models import IndexedPage
from .searching import tokenize, search_pages


class SearchTests(TestCase):
    def setUp(self):
        IndexedPage.objects.create(
            title="Learn Django with Python",
            url="https://example.org/django",
            description="A beginner Django tutorial",
            body_text="Python web development framework tutorial",
        )
        IndexedPage.objects.create(
            title="Garden plants guide",
            url="https://example.org/garden",
            description="How to grow plants",
            body_text="Gardening tips and outdoor plants",
        )

    def test_tokenize_removes_common_words(self):
        self.assertEqual(tokenize("the Python and Django"), ["python", "django"])

    def test_search_ranks_relevant_title(self):
        results = search_pages("Django Python")
        self.assertTrue(results)
        self.assertEqual(results[0]["page"].title, "Learn Django with Python")

    def test_home_page_loads(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_search_results_page_loads(self):
        response = self.client.get(reverse("results"), {"q": "Django"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Learn Django with Python")
