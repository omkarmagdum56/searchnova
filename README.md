# SearchNova — Django Web Search Engine

SearchNova is a local, portfolio-ready search engine prototype built with Django. It includes a search UI, searchable page index, keyword relevance ranking, query history, a robots.txt-aware crawler, seed URL management, and Django admin.

> Scope: this is a focused crawler/index for a small set of public websites, not a full copy of Google's global index. Crawl only sites you are allowed to access. Respect robots.txt, terms of service, and rate limits.

## Requirements
- Windows 10/11
- Python 3.10+ (Python 3.11 or 3.12 recommended)
- Internet connection for crawling public pages

## Run on Windows (Command Prompt)
1. Extract the ZIP to a folder such as `C:\Users\DELL\Desktop\SearchNova`.
2. Open Command Prompt in that folder.
3. Create a virtual environment:
   ```bat
   py -m venv .venv
   .venv\Scripts\activate
   ```
4. Install packages:
   ```bat
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```
5. Create database tables and an admin account:
   ```bat
   python manage.py migrate
   python manage.py createsuperuser
   ```
6. Load starter records so searches return sample results immediately:
   ```bat
   python manage.py load_demo_index
   ```
7. Start the development server:
   ```bat
   python manage.py runserver
   ```
8. Open `http://127.0.0.1:8000/` in your browser. Admin: `http://127.0.0.1:8000/admin/`.

The starter records point to official documentation sites and are sample index entries for testing. They are not a live crawl. Use the crawler below to fetch permitted live page content.

## Add pages to the index
1. Sign in at `/admin/`.
2. Under **Search → Crawl seeds**, add a public HTTP/HTTPS URL and save it.
3. Run:
   ```bat
   python manage.py crawl_sites --max-pages 10
   ```
4. Return to the home page and search for words that occur on those pages.

The crawler checks robots.txt, limits pages per seed, restricts crawling to the seed's hostname, uses a request timeout, and skips non-public/private IP destinations. Start with a small `--max-pages` value.

## Included features
- Responsive SearchNova homepage and results page
- Query normalization and basic relevance scoring
- Indexed page title, URL, description, body text, and crawl timestamp
- Search history for analytics
- Crawl seeds editable in Django admin
- Management command for controlled crawling
- Django admin for indexed pages and search history
- Basic security defaults and CSRF protection

## Current limitations / next upgrades
- No global internet index, distributed crawler, PageRank, or image/news verticals yet.
- SQLite and simple text matching are intended for local demonstration.
- For production, add robust SSRF/DNS-rebinding defenses, background jobs, crawl scheduling, deduplication by canonical URL/content hash, language detection, rate limiting, tests, monitoring, and PostgreSQL full-text search.


## SearchNova Professional UI update

The refreshed interface keeps the existing Django search workflow and adds a staff-only analytics page.

- Home: `/`
- Search results: `/search/?q=python`
- Staff analytics: `/analytics/` (sign in with a Django staff/superuser account)
- Django admin: `/admin/`

### Install and run on Windows

1. Open this folder in VS Code.
2. Create/activate your virtual environment.
3. Install dependencies: `pip install -r requirements.txt`
4. Run: `python manage.py check`
5. Start: `python manage.py runserver`

The existing SQLite database is included in this project archive. Keep a backup of `db.sqlite3` before making database changes.
