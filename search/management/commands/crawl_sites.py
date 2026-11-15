import hashlib
import ipaddress
import socket
import time
from urllib.parse import urljoin, urlparse, urldefrag
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from django.utils import timezone

from search.models import CrawlSeed, IndexedPage

USER_AGENT = "SearchNovaBot/1.0 (+local portfolio crawler)"
REQUEST_TIMEOUT = 8
MAX_BODY_CHARS = 20000
MAX_HTML_BYTES = 1_500_000


def is_public_http_url(url):
    """Reject non-http schemes, credentials, localhost, and private/reserved IPs."""
    try:
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"} or not parsed.hostname:
            return False
        if parsed.username or parsed.password:
            return False
        host = parsed.hostname.lower().rstrip(".")
        if host == "localhost" or host.endswith(".localhost") or host.endswith(".local"):
            return False
        try:
            addresses = {ipaddress.ip_address(host)}
        except ValueError:
            try:
                resolved = socket.getaddrinfo(host, None, type=socket.SOCK_STREAM)
                addresses = {ipaddress.ip_address(item[4][0]) for item in resolved}
            except (OSError, ValueError):
                return False
        return bool(addresses) and all(ip.is_global for ip in addresses)
    except (ValueError, TypeError):
        return False


def robots_allows(url):
    parsed = urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    parser = RobotFileParser()
    parser.set_url(robots_url)
    try:
        response = requests.get(
            robots_url, headers={"User-Agent": USER_AGENT},
            timeout=REQUEST_TIMEOUT, allow_redirects=False
        )
        if response.status_code in (401, 403):
            return False
        if response.status_code >= 400:
            return True
        parser.parse(response.text.splitlines())
        return parser.can_fetch(USER_AGENT, url)
    except requests.RequestException:
        # Fail closed when robots.txt cannot be checked.
        return False


class Command(BaseCommand):
    help = "Crawl enabled seed URLs and index a small number of public HTML pages."

    def add_arguments(self, parser):
        parser.add_argument("--max-pages", type=int, default=10)
        parser.add_argument("--delay", type=float, default=1.0)

    def handle(self, *args, **options):
        max_pages = max(1, min(options["max_pages"], 100))
        delay = max(1.0, min(options["delay"], 10.0))
        seeds = CrawlSeed.objects.filter(enabled=True)
        if not seeds.exists():
            self.stdout.write(self.style.WARNING(
                "No enabled seeds. Add a URL at /admin/ → Search → Crawl seeds."
            ))
            return

        session = requests.Session()
        session.headers.update({"User-Agent": USER_AGENT})
        indexed = 0

        for seed in seeds:
            start = seed.url
            if not is_public_http_url(start):
                self.stderr.write(f"Skipped unsafe/non-public URL: {start}")
                continue
            host = urlparse(start).hostname
            queue, seen = [start], set()

            while queue and indexed < max_pages:
                url = urldefrag(queue.pop(0))[0]
                if url in seen:
                    continue
                seen.add(url)
                parsed = urlparse(url)
                if parsed.hostname != host or not is_public_http_url(url):
                    continue
                if not robots_allows(url):
                    self.stdout.write(f"Robots policy disallows or could not verify: {url}")
                    continue

                try:
                    response = session.get(
                        url, timeout=REQUEST_TIMEOUT, allow_redirects=False,
                        stream=True
                    )
                    if response.is_redirect:
                        location = response.headers.get("Location")
                        if location:
                            redirected = urljoin(url, location)
                            if urlparse(redirected).hostname == host and redirected not in seen:
                                queue.append(redirected)
                        response.close()
                        time.sleep(delay)
                        continue

                    content_type = response.headers.get("Content-Type", "").lower()
                    if response.status_code != 200 or "text/html" not in content_type:
                        response.close()
                        time.sleep(delay)
                        continue

                    chunks, total = [], 0
                    for chunk in response.iter_content(chunk_size=16384):
                        total += len(chunk)
                        if total > MAX_HTML_BYTES:
                            break
                        chunks.append(chunk)
                    encoding = response.encoding or "utf-8"
                    html = b"".join(chunks).decode(encoding, errors="replace")
                    response.close()
                except requests.RequestException as exc:
                    self.stderr.write(f"Request failed for {url}: {exc}")
                    time.sleep(delay)
                    continue

                soup = BeautifulSoup(html, "html.parser")
                for tag in soup(["script", "style", "noscript", "svg", "nav", "footer"]):
                    tag.decompose()

                title_tag = soup.find("title")
                title = title_tag.get_text(" ", strip=True)[:300] if title_tag else ""
                meta = soup.find("meta", attrs={"name": lambda v: v and v.lower() == "description"})
                description = (meta.get("content", "") if meta else "")[:500]
                body_text = " ".join(soup.get_text(" ", strip=True).split())[:MAX_BODY_CHARS]
                digest = hashlib.sha256(body_text.encode("utf-8")).hexdigest()

                IndexedPage.objects.update_or_create(
                    url=url,
                    defaults={
                        "title": title or url,
                        "description": description,
                        "body_text": body_text,
                        "content_hash": digest,
                        "status_code": response.status_code,
                        "crawled_at": timezone.now(),
                    },
                )
                indexed += 1
                self.stdout.write(self.style.SUCCESS(f"Indexed: {title or url}"))

                for anchor in soup.find_all("a", href=True):
                    target = urldefrag(urljoin(url, anchor["href"]))[0]
                    target_parsed = urlparse(target)
                    if (target_parsed.scheme in {"http", "https"}
                        and target_parsed.hostname == host
                        and target not in seen and len(queue) < 500):
                        queue.append(target)

                time.sleep(delay)
                if indexed >= max_pages:
                    break

        self.stdout.write(self.style.SUCCESS(f"Crawl finished. Pages processed: {indexed}"))
