# 🔎 SearchNova — AI-Powered Web Search Engine

### Discover the Web. Search Smarter.

SearchNova is a Python and Django-based web search engine that combines hybrid search, custom web crawling, locally running Artificial Intelligence, search analytics, and voice-based search in one platform.

It allows users to search indexed web pages, retrieve external results through DuckDuckGo fallback, and generate AI-powered overviews using Ollama and Llama 3.2.

---

## 🚀 Project Highlights

| Feature | Technology |
|---|---|
| Hybrid Search | Django + DuckDuckGo |
| AI Overview | Ollama + Llama 3.2 |
| Web Crawling | Python |
| Search Indexing | Django ORM |
| Search Analytics | Django + SQLite |
| Smart Suggestions | JavaScript |
| Voice Search | Web Speech API |
| Admin Management | Django Admin |

---

## ✨ Powerful Features

### 1. Hybrid Search Engine

- Search web pages from the internal database.
- DuckDuckGo API fallback when local results are unavailable.
- Support for multiple search sources.
- Search relevance scoring.
- Title and description matching.
- Search results organized by categories.

### 2. AI Overview – Ollama

- Local AI integration using Llama 3.2.
- Generate AI answers based on search results.
- AI-generated search summaries.
- Database-based AI response caching.
- Local AI processing without requiring Gemini API.
- Reduced repeated AI processing through caching.

### 3. Custom Web Crawler

- Crawl websites using configured seed URLs.
- Extract page titles, descriptions, and HTML content.
- Save crawled pages into the database.
- Check robots.txt before crawling.
- Domain restrictions for controlled crawling.
- Store content hashes to identify page content changes.

### 4. Search Analytics Dashboard

- Total searches.
- Today's searches.
- Unique search queries.
- Searches with no results.
- Top 10 search keywords.
- Last 7 days search activity.
- Search activity monitoring.

### 5. Smart Search Suggestions

- Automatic search suggestions.
- Previous search history.
- Recent search selection.
- Delete previous search history.
- Faster search navigation.

### 6. Voice Search

- Microphone-based search.
- Speech-to-text functionality.
- Automatically submit voice queries.
- Browser-based speech recognition support.

### 7. Advanced Search Capabilities

- Search relevance scoring.
- Title and description matching.
- All, Tech, and News categories.
- Search pagination (10 results per page).
- Indexed page content hashing.
- Database-backed search history.
- Search result filtering.

### 8. Django Administration

- Manage indexed web pages.
- View search records.
- Manage crawler seed URLs.
- Monitor indexed content.
- Manage search engine database records.

### 9. Responsive User Interface

- Modern search engine interface.
- Clean and professional design.
- Responsive layouts.
- User-friendly navigation.
- Search-focused interface.

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend Programming |
| Django | Web Framework |
| SQLite | Database |
| HTML5 | Page Structure |
| CSS3 | Styling |
| JavaScript | Frontend Interactions |
| Bootstrap (if configured) | UI Components |
| Ollama | Local AI Runtime |
| Llama 3.2 | Language Model |
| DuckDuckGo | External Search Fallback |
| Web Speech API | Voice Search |
| Git & GitHub | Version Control |

---

## 🏗️ Project Architecture

```text
                 USER
                   |
                   v
             SEARCH INTERFACE
                   |
                   v
             DJANGO APPLICATION
                   |
          +--------+---------+
          |                  |
          v                  v
     LOCAL SEARCH       DUCKDUCKGO
          |               FALLBACK
          v                  |
      SQLITE DATABASE <------+
          |
          v
     SEARCH RESULTS
          |
          v
       OLLAMA AI
       LLAMA 3.2
          |
          v
      AI OVERVIEW
```

### Web Crawling Workflow

```text
Seed URLs
    |
    v
Web Crawler
    |
    v
robots.txt Check
    |
    v
HTML Extraction
    |
    v
Content Processing
    |
    v
Database Indexing
    |
    v
Searchable Web Pages
```

---

## 📁 Project Structure

```text
SearchNova/
│
├── search/
│   ├── management/
│   │   └── commands/
│   │       ├── crawl_sites.py
│   │       └── load_demo_index.py
│   │
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── searching.py
│   ├── services.py
│   ├── tests.py
│   └── views.py
│
├── searchnova/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── static/
├── templates/
│
├── .gitignore
├── LICENSE
├── README.md
├── manage.py
└── requirements.txt
```

---

## ⚙️ Installation & Setup

### Prerequisites

- Python 3.10 or compatible version.
- pip package manager.
- Git.
- Ollama for local AI functionality.
- Windows 10/11 or compatible operating system.

### Step 1: Clone Repository

```bash
git clone https://github.com/omkarmagdum56/searchnova.git
```

### Step 2: Open Project Directory

```bash
cd searchnova
```

### Step 3: Create Virtual Environment

```bash
python -m venv venv
```

### Step 4: Activate Virtual Environment

Windows CMD:

```cmd
venv\Scripts\activate
```

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 6: Apply Database Migrations

```bash
python manage.py migrate
```

### Step 7: Load Demo Data (Optional)

```bash
python manage.py load_demo_index
```

### Step 8: Create Django Superuser

```bash
python manage.py createsuperuser
```

### Step 9: Run Development Server

```bash
python manage.py runserver
```

Open the application:

http://127.0.0.1:8000/

---

## 🤖 Ollama & Llama 3.2 Setup

SearchNova uses Ollama to run AI models locally.

### Step 1: Install Ollama

Download Ollama:

https://ollama.com/download

### Step 2: Download Llama 3.2

Open CMD:

```bash
ollama pull llama3.2
```

### Step 3: Start Ollama

```bash
ollama serve
```

If Ollama is already running as a background application, you may not need to start it manually.

### Step 4: Verify Model

```bash
ollama list
```

### Step 5: Test Model

```bash
ollama run llama3.2
```

Enter a test prompt to verify that the model responds.

**Note:** The exact Ollama model name and connection configuration must match the application's AI service settings.

---

## 🕷️ Web Crawling

SearchNova includes custom Django management commands for crawling and indexing web pages.

### Crawl Websites

```bash
python manage.py crawl_sites
```

### Load Demo Indexed Pages

```bash
python manage.py load_demo_index
```

Check available command options:

```bash
python manage.py help crawl_sites
```

Always respect website robots.txt rules, crawling restrictions, and server rate limits.

---

## 📊 Search Analytics

The analytics dashboard provides information about:

- Total search activity.
- Daily search activity.
- Unique search queries.
- Searches returning no results.
- Most frequently searched keywords.
- Seven-day search trends.

These insights help monitor search engine usage and understand user search behaviour.

---

## 🎤 Voice Search

SearchNova provides microphone-based search through browser speech recognition.

Voice search functionality depends on browser compatibility and microphone permissions.

---

## 🔐 Security & Configuration

- Do not upload API keys, passwords, or secret credentials.
- Keep local environment variables in `.env`.
- Exclude virtual environments and local database files from Git.
- Use appropriate Django production security settings before deployment.
- Do not expose Django SECRET_KEY or DEBUG settings in production.

---

## 🔮 Future Enhancements

- Advanced search ranking algorithms.
- Better semantic search capabilities.
- Search autocomplete improvements.
- Enhanced AI answer quality.
- More advanced crawler scheduling.
- Improved indexing performance.
- User authentication and personalized search.
- Search filters and sorting improvements.
- Production deployment and scalability.

---

## 🎯 Project Objectives

1. Understand how search engines collect and index web content.
2. Implement custom web crawling using Python.
3. Develop a hybrid search engine using Django.
4. Integrate locally hosted Artificial Intelligence.
5. Implement search analytics and monitoring.
6. Explore voice-based search functionality.
7. Build a practical, real-world software development project.

---

## 👨‍💻 Developer

**Onkar Magdum**

Python & Django Developer

GitHub: https://github.com/omkarmagdum56

Project Repository:

https://github.com/omkarmagdum56/searchnova

---

## 📜 License

This project is distributed under the license included in this repository.

---

### SearchNova

**Discover the Web. Search Smarter.**

Built with Python, Django, and Local AI.
