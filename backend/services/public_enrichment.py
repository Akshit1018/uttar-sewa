"""Public enrichment sources listed in public-apis, plus a safe HTML fetch.

Video answers stay grounded in the corpus. These payloads are companions only:
they must be labeled `public` and never mixed into `/api/ask` answer text.

Sources (from https://github.com/public-apis/public-apis):
- Bhagavad Gita (vedicscriptures / gita-api.vercel.app)
- Wikipedia REST
- Free Dictionary
- Sunrise-Sunset (sandhya)
- Open Library
- YouTube oEmbed

HTML fetch uses Scrapling Fetcher when installed, otherwise httpx.
Stealth/anti-bot fetchers are not used.
"""

from __future__ import annotations

import ipaddress
import re
from datetime import date, datetime, timezone
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import quote, urlparse

import httpx

try:
    from scrapling.fetchers import Fetcher as ScraplingFetcher
except ImportError:
    ScraplingFetcher = None

GITA_VERSES_PER_CHAPTER = (0, 47, 72, 43, 42, 29, 47, 30, 28, 34, 42, 55, 20, 35, 27, 20, 24, 28, 78)
GITA_TOTAL = sum(GITA_VERSES_PER_CHAPTER)
VARANASI = (25.3176, 82.9739)

ALLOWED_HOSTS = {
    "vedicscriptures.github.io",
    "gita-api.vercel.app",
    "en.wikipedia.org",
    "hi.wikipedia.org",
    "api.dictionaryapi.dev",
    "api.sunrise-sunset.org",
    "openlibrary.org",
    "www.youtube.com",
    "youtube.com",
    "zenquotes.io",
}

PUBLIC_CATALOG = [
    {
        "id": "gita",
        "name": "Bhagavad Gita",
        "listed_in": "https://github.com/public-apis/public-apis",
        "endpoint": "https://vedicscriptures.github.io/slok/{chapter}/{verse}",
        "auth": "none",
    },
    {
        "id": "wikipedia",
        "name": "Wikipedia",
        "listed_in": "https://github.com/public-apis/public-apis",
        "endpoint": "https://{lang}.wikipedia.org/api/rest_v1/page/summary/{title}",
        "auth": "none",
    },
    {
        "id": "dictionary",
        "name": "Free Dictionary",
        "listed_in": "https://github.com/public-apis/public-apis",
        "endpoint": "https://api.dictionaryapi.dev/api/v2/entries/en/{word}",
        "auth": "none",
    },
    {
        "id": "sunrise",
        "name": "Sunrise and Sunset",
        "listed_in": "https://github.com/public-apis/public-apis",
        "endpoint": "https://api.sunrise-sunset.org/json",
        "auth": "none",
    },
    {
        "id": "open_library",
        "name": "Open Library",
        "listed_in": "https://github.com/public-apis/public-apis",
        "endpoint": "https://openlibrary.org/search.json",
        "auth": "none",
    },
    {
        "id": "youtube_oembed",
        "name": "YouTube oEmbed",
        "listed_in": "https://github.com/public-apis/public-apis",
        "endpoint": "https://www.youtube.com/oembed",
        "auth": "none",
    },
]

_GITA_REF = re.compile(
    r"(?:gita|गीता|गीता)\s*(?:chapter\s*)?(\d{1,2})\s*[:.\-–]\s*(\d{1,3})",
    re.IGNORECASE,
)


def catalog() -> List[Dict[str, str]]:
    return [dict(item) for item in PUBLIC_CATALOG]


def daily_gita_ref(on: Optional[date] = None) -> Tuple[int, int]:
    day = (on or date.today()).timetuple().tm_yday
    index = (day - 1) % GITA_TOTAL
    for chapter, count in enumerate(GITA_VERSES_PER_CHAPTER):
        if chapter == 0:
            continue
        if index < count:
            return chapter, index + 1
        index -= count
    return 18, 78


def extract_gita_ref(query: str) -> Optional[Tuple[int, int]]:
    match = _GITA_REF.search(query or "")
    if not match:
        return None
    chapter = int(match.group(1))
    verse = int(match.group(2))
    if chapter < 1 or chapter > 18:
        return None
    if verse < 1 or verse > GITA_VERSES_PER_CHAPTER[chapter]:
        return None
    return chapter, verse


def parse_gita_payload(data: Dict[str, Any], language: str = "hi") -> Dict[str, Any]:
    chapter = int(data.get("chapter") or 0)
    verse = int(data.get("verse") or 0)
    hindi = ""
    english = ""
    tej = data.get("tej") or {}
    siva = data.get("siva") or {}
    if isinstance(tej, dict):
        hindi = (tej.get("ht") or tej.get("author") or "") if isinstance(tej.get("ht"), str) else ""
        if not hindi:
            hindi = str(tej.get("ht") or "")
    if isinstance(siva, dict):
        english = str(siva.get("et") or "")
    text = hindi if language == "hi" and hindi else (english or hindi or str(data.get("slok") or ""))
    return {
        "kind": "gita",
        "source": "public",
        "title": f"Bhagavad Gita {chapter}.{verse}",
        "text": text.strip(),
        "sanskrit": str(data.get("slok") or "").strip(),
        "url": f"https://vedicscriptures.github.io/slok/{chapter}/{verse}",
        "attribution": "Bhagavad Gita API (public-apis) — not from Uttar Sewa videos",
        "chapter": chapter,
        "verse": verse,
    }


def parse_wikipedia_summary(data: Dict[str, Any]) -> Dict[str, Any]:
    title = str(data.get("title") or "")
    extract = str(data.get("extract") or "")
    url = ""
    content_urls = data.get("content_urls") or {}
    desktop = content_urls.get("desktop") if isinstance(content_urls, dict) else {}
    if isinstance(desktop, dict):
        url = str(desktop.get("page") or "")
    return {
        "kind": "wikipedia",
        "source": "public",
        "title": title,
        "text": extract.strip(),
        "url": url,
        "attribution": "Wikipedia (public-apis) — not from Uttar Sewa videos",
    }


def parse_dictionary_payload(data: Any) -> Dict[str, Any]:
    entries = data if isinstance(data, list) else [data]
    first = entries[0] if entries and isinstance(entries[0], dict) else {}
    word = str(first.get("word") or "")
    meanings = first.get("meanings") or []
    definition = ""
    if meanings and isinstance(meanings[0], dict):
        defs = meanings[0].get("definitions") or []
        if defs and isinstance(defs[0], dict):
            definition = str(defs[0].get("definition") or "")
    return {
        "kind": "dictionary",
        "source": "public",
        "title": word,
        "text": definition.strip(),
        "url": f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}" if word else "",
        "attribution": "Free Dictionary (public-apis) — not from Uttar Sewa videos",
    }


def parse_sunrise_payload(data: Dict[str, Any]) -> Dict[str, Any]:
    results = data.get("results") if isinstance(data.get("results"), dict) else {}
    sunrise = str(results.get("sunrise") or "")
    sunset = str(results.get("sunset") or "")
    return {
        "kind": "sandhya",
        "source": "public",
        "title": "Sandhya",
        "sunrise": sunrise,
        "sunset": sunset,
        "text": f"Sunrise {sunrise} · Sunset {sunset}".strip(" ·"),
        "url": "https://sunrise-sunset.org/api",
        "attribution": "Sunrise-Sunset (public-apis) — local sandhya window, not a video teaching",
    }


def parse_open_library_payload(data: Dict[str, Any], limit: int = 3) -> List[Dict[str, Any]]:
    docs = data.get("docs") if isinstance(data.get("docs"), list) else []
    books = []
    for item in docs[:limit]:
        if not isinstance(item, dict):
            continue
        title = str(item.get("title") or "")
        key = str(item.get("key") or "")
        authors = item.get("author_name") or []
        author = authors[0] if authors else ""
        books.append(
            {
                "kind": "book",
                "source": "public",
                "title": title,
                "text": f"{title} — {author}".strip(" —"),
                "url": f"https://openlibrary.org{key}" if key else "https://openlibrary.org",
                "attribution": "Open Library (public-apis) — not from Uttar Sewa videos",
            }
        )
    return books


def parse_youtube_oembed(data: Dict[str, Any], video_id: str = "") -> Dict[str, Any]:
    title = str(data.get("title") or "")
    author = str(data.get("author_name") or "")
    watch = f"https://www.youtube.com/watch?v={video_id}" if video_id else str(data.get("author_url") or "")
    return {
        "kind": "youtube_meta",
        "source": "public",
        "title": title,
        "text": f"{title} — {author}".strip(" —"),
        "url": watch,
        "attribution": "YouTube oEmbed (public-apis) — metadata only, not a transcript",
        "video_id": video_id,
        "author": author,
    }


def is_safe_public_url(url: str) -> bool:
    parsed = urlparse(url or "")
    if parsed.scheme not in ("http", "https"):
        return False
    host = (parsed.hostname or "").lower()
    if host not in ALLOWED_HOSTS:
        return False
    try:
        ip = ipaddress.ip_address(host)
    except ValueError:
        return True
    return not (ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved)


def companion_disclaimer(language: str = "hi") -> str:
    if language == "hi":
        return "यह सार्वजनिक पाठ है, प्रवचन-वीडियो नहीं। उत्तर ऊपर केवल वीडियो से है।"
    return "This is a public text, not a discourse video. The answer above is from videos only."


def build_companions(
    query: str,
    language: str = "hi",
    gita: Optional[Dict[str, Any]] = None,
    wiki: Optional[Dict[str, Any]] = None,
    definition: Optional[Dict[str, Any]] = None,
    books: Optional[List[Dict[str, Any]]] = None,
    sandhya: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    """Corrective-RAG style: extra public cards, never the video answer."""
    cards: List[Dict[str, Any]] = []
    if gita and gita.get("text"):
        cards.append(gita)
    if wiki and wiki.get("text"):
        cards.append(wiki)
    if definition and definition.get("text"):
        cards.append(definition)
    for book in books or []:
        if book.get("text"):
            cards.append(book)
    if sandhya and sandhya.get("text"):
        cards.append(sandhya)
    for card in cards:
        card["source"] = "public"
        card["disclaimer"] = companion_disclaimer(language)
        card["query"] = query
    return cards


def wiki_title_from_query(query: str) -> str:
    cleaned = re.sub(r"\s+", " ", (query or "").strip())
    return cleaned[:80] or "Meditation"


def dictionary_word(query: str) -> str:
    match = re.search(r"[A-Za-z]{3,}", query or "")
    if match:
        return match.group(0).lower()
    mapping = {
        "ध्यान": "meditation",
        "भक्ति": "devotion",
        "कर्म": "karma",
        "मोक्ष": "moksha",
        "गुरु": "guru",
        "माला": "mala",
        "जप": "japa",
    }
    for hindi, english in mapping.items():
        if hindi in (query or ""):
            return english
    return "meditation"


class PublicHttp:
    def __init__(self, timeout: float = 8.0):
        self.timeout = timeout

    def get_json(self, url: str) -> Any:
        if not is_safe_public_url(url):
            raise ValueError("blocked url")
        with httpx.Client(timeout=self.timeout, follow_redirects=False) as client:
            response = client.get(url, headers={"User-Agent": "UttarSewa/2.3"})
            response.raise_for_status()
            return response.json()

    def get_text(self, url: str) -> str:
        if not is_safe_public_url(url):
            raise ValueError("blocked url")
        if ScraplingFetcher is not None:
            page = ScraplingFetcher.get(url)
            html = getattr(page, "html", None) or str(page)
            title = ""
            text = ""
            try:
                title = page.css("title::text").get() or ""
                text = " ".join(page.css("p::text").getall()[:12])
            except Exception:
                text = html[:2000]
            return f"{title}\n{text}".strip()
        with httpx.Client(timeout=self.timeout, follow_redirects=False) as client:
            response = client.get(url, headers={"User-Agent": "UttarSewa/2.3"})
            response.raise_for_status()
            return response.text[:8000]


def fetch_gita(chapter: int, verse: int, language: str = "hi", http: Optional[PublicHttp] = None) -> Dict[str, Any]:
    client = http or PublicHttp()
    url = f"https://vedicscriptures.github.io/slok/{chapter}/{verse}"
    return parse_gita_payload(client.get_json(url), language=language)


def fetch_wikipedia(query: str, language: str = "hi", http: Optional[PublicHttp] = None) -> Dict[str, Any]:
    client = http or PublicHttp()
    lang = "hi" if language == "hi" else "en"
    title = wiki_title_from_query(query)
    url = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{quote(title)}"
    return parse_wikipedia_summary(client.get_json(url))


def fetch_definition(query: str, http: Optional[PublicHttp] = None) -> Dict[str, Any]:
    client = http or PublicHttp()
    word = dictionary_word(query)
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    return parse_dictionary_payload(client.get_json(url))


def fetch_sandhya(lat: float = VARANASI[0], lng: float = VARANASI[1], http: Optional[PublicHttp] = None) -> Dict[str, Any]:
    client = http or PublicHttp()
    url = f"https://api.sunrise-sunset.org/json?lat={lat}&lng={lng}&formatted=0"
    return parse_sunrise_payload(client.get_json(url))


def fetch_books(query: str, http: Optional[PublicHttp] = None) -> List[Dict[str, Any]]:
    client = http or PublicHttp()
    q = quote(wiki_title_from_query(query) or "bhakti")
    url = f"https://openlibrary.org/search.json?q={q}&limit=3"
    return parse_open_library_payload(client.get_json(url))


def fetch_youtube_meta(video_id: str, http: Optional[PublicHttp] = None) -> Dict[str, Any]:
    client = http or PublicHttp()
    watch = f"https://www.youtube.com/watch?v={video_id}"
    url = f"https://www.youtube.com/oembed?url={watch}&format=json"
    return parse_youtube_oembed(client.get_json(url), video_id=video_id)


def scrape_public_page(url: str, http: Optional[PublicHttp] = None) -> Dict[str, Any]:
    client = http or PublicHttp()
    if not is_safe_public_url(url):
        raise ValueError("only allowlisted public hosts can be scraped")
    text = client.get_text(url)
    title = text.split("\n", 1)[0][:120]
    body = text[len(title) :].strip() if text.startswith(title) else text
    return {
        "kind": "scrape",
        "source": "public",
        "title": title or url,
        "text": body[:2000],
        "url": url,
        "attribution": "Scrapling/httpx public fetch — not from Uttar Sewa videos",
        "engine": "scrapling" if ScraplingFetcher is not None else "httpx",
    }


def today_bundle(language: str = "hi", http: Optional[PublicHttp] = None, on: Optional[date] = None) -> Dict[str, Any]:
    chapter, verse = daily_gita_ref(on)
    gita = None
    sandhya = None
    try:
        gita = fetch_gita(chapter, verse, language=language, http=http)
    except Exception:
        gita = {
            "kind": "gita",
            "source": "public",
            "title": f"Bhagavad Gita {chapter}.{verse}",
            "text": "",
            "chapter": chapter,
            "verse": verse,
            "url": f"https://vedicscriptures.github.io/slok/{chapter}/{verse}",
            "attribution": "Bhagavad Gita API unavailable right now",
        }
    try:
        sandhya = fetch_sandhya(http=http)
    except Exception:
        sandhya = {"kind": "sandhya", "source": "public", "text": "", "sunrise": "", "sunset": ""}
    return {
        "date": (on or date.today()).isoformat(),
        "gita": gita,
        "sandhya": sandhya,
        "catalog": catalog(),
        "disclaimer": companion_disclaimer(language),
        "scrapling": ScraplingFetcher is not None,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


def companions_for_query(query: str, language: str = "hi", http: Optional[PublicHttp] = None) -> List[Dict[str, Any]]:
    ref = extract_gita_ref(query) or daily_gita_ref()
    gita = wiki = definition = None
    books: List[Dict[str, Any]] = []
    try:
        gita = fetch_gita(ref[0], ref[1], language=language, http=http)
    except Exception:
        gita = None
    try:
        wiki = fetch_wikipedia(query, language=language, http=http)
    except Exception:
        wiki = None
    try:
        definition = fetch_definition(query, http=http)
    except Exception:
        definition = None
    try:
        books = fetch_books(query, http=http)
    except Exception:
        books = []
    return build_companions(query, language, gita=gita, wiki=wiki, definition=definition, books=books)
