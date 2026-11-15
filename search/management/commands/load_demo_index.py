from django.core.management.base import BaseCommand
from django.utils import timezone
from search.models import IndexedPage

DEMO_PAGES = [
    {"title": "Python Documentation", "url": "https://docs.python.org/3/", "description": "Official Python documentation, tutorials, language reference and library guides.", "body_text": "Python is a programming language. Learn Python syntax, data types, functions, classes, modules, exceptions, file handling and standard library tools. Python is widely used for web development, automation, data science and scripting."},
    {"title": "Django Documentation", "url": "https://docs.djangoproject.com/en/5.2/", "description": "Official Django documentation for building secure and maintainable web applications.", "body_text": "Django is a high-level Python web framework. Learn models, views, templates, URL routing, forms, authentication, database migrations, ORM queries, static files and deployment."},
    {"title": "HTML: HyperText Markup Language", "url": "https://developer.mozilla.org/en-US/docs/Web/HTML", "description": "Learn HTML elements and structure for web pages.", "body_text": "HTML defines the structure and meaning of web content. Learn elements, headings, paragraphs, links, images, forms, semantic markup and accessibility."},
    {"title": "CSS: Cascading Style Sheets", "url": "https://developer.mozilla.org/en-US/docs/Web/CSS", "description": "Learn how CSS styles and layouts web pages.", "body_text": "CSS controls presentation of HTML documents. Learn selectors, colors, typography, box model, flexbox, grid, responsive design, transitions and layouts."},
    {"title": "JavaScript Guide", "url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide", "description": "A guide to the JavaScript programming language.", "body_text": "JavaScript adds interaction to websites. Learn variables, functions, arrays, objects, events, DOM manipulation, promises, asynchronous programming and modules."},
]

class Command(BaseCommand):
    help = "Load a small clearly-labelled starter index so SearchNova can be tested immediately."

    def handle(self, *args, **options):
        created = 0
        for item in DEMO_PAGES:
            _, was_created = IndexedPage.objects.update_or_create(
                url=item["url"], defaults={**item, "status_code": 200, "crawled_at": timezone.now()}
            )
            created += int(was_created)
        self.stdout.write(self.style.SUCCESS(
            f"Starter index ready: {len(DEMO_PAGES)} demo pages available ({created} newly added). "
            "These are sample index records; run crawl_sites to fetch and index live page content."
        ))
