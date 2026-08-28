from backend.services.public_enrichment import (
    build_companions,
    catalog,
    companion_disclaimer,
    daily_gita_ref,
    dictionary_word,
    extract_gita_ref,
    is_safe_public_url,
    parse_dictionary_payload,
    parse_gita_payload,
    parse_open_library_payload,
    parse_sunrise_payload,
    parse_wikipedia_summary,
    parse_youtube_oembed,
    scrape_public_page,
)


GITA_FIXTURE = {
    "chapter": 2,
    "verse": 47,
    "slok": "कर्मण्येवाधिकारस्ते मा फलेषु कदाचन।",
    "tej": {"ht": "कर्म करने में तुम्हारा अधिकार है, फल में नहीं।"},
    "siva": {"et": "You have a right to action, never to its fruits."},
}


class FakeHttp:
    def __init__(self, json_by_url=None, text_by_url=None):
        self.json_by_url = json_by_url or {}
        self.text_by_url = text_by_url or {}

    def get_json(self, url: str):
        for key, value in self.json_by_url.items():
            if key in url:
                return value
        raise KeyError(url)

    def get_text(self, url: str):
        for key, value in self.text_by_url.items():
            if key in url:
                return value
        raise KeyError(url)


def test_daily_gita_ref_is_in_range():
    chapter, verse = daily_gita_ref()
    assert 1 <= chapter <= 18
    assert verse >= 1


def test_extract_gita_ref_from_hindi_query():
    assert extract_gita_ref("गीता 2.47 क्या कहती है") == (2, 47)
    assert extract_gita_ref("gita 18:66") == (18, 66)
    assert extract_gita_ref("random") is None


def test_parse_gita_prefers_hindi():
    card = parse_gita_payload(GITA_FIXTURE, language="hi")
    assert card["source"] == "public"
    assert "फल" in card["text"]
    assert card["kind"] == "gita"
    assert "not from Uttar Sewa videos" in card["attribution"]


def test_parse_wikipedia_and_dictionary():
    wiki = parse_wikipedia_summary(
        {
            "title": "Meditation",
            "extract": "Meditation is a practice.",
            "content_urls": {"desktop": {"page": "https://en.wikipedia.org/wiki/Meditation"}},
        }
    )
    assert wiki["kind"] == "wikipedia"
    assert wiki["url"].startswith("https://en.wikipedia.org")
    definition = parse_dictionary_payload(
        [{"word": "karma", "meanings": [{"definitions": [{"definition": "action and its result"}]}]}]
    )
    assert definition["title"] == "karma"
    assert "action" in definition["text"]


def test_parse_sunrise_and_books_and_oembed():
    sandhya = parse_sunrise_payload(
        {"results": {"sunrise": "2026-08-12T00:30:00+00:00", "sunset": "2026-08-12T13:00:00+00:00"}}
    )
    assert sandhya["kind"] == "sandhya"
    books = parse_open_library_payload(
        {"docs": [{"title": "Bhagavad Gita", "key": "/works/OL1W", "author_name": ["Eknath Easwaran"]}]}
    )
    assert books[0]["kind"] == "book"
    meta = parse_youtube_oembed({"title": "Satsang", "author_name": "Bhajan Marg"}, video_id="abc")
    assert meta["video_id"] == "abc"
    assert "metadata only" in meta["attribution"]


def test_companions_are_labeled_public_and_not_video_answers():
    cards = build_companions(
        "ध्यान",
        language="hi",
        gita=parse_gita_payload(GITA_FIXTURE, "hi"),
        wiki=parse_wikipedia_summary({"title": "Dhyana", "extract": "ध्यान एक अभ्यास है।"}),
    )
    assert cards
    assert all(card["source"] == "public" for card in cards)
    assert all("प्रवचन-वीडियो नहीं" in card["disclaimer"] for card in cards)
    assert companion_disclaimer("en").startswith("This is a public text")


def test_scrape_blocks_private_hosts():
    assert is_safe_public_url("https://en.wikipedia.org/wiki/Karma") is True
    assert is_safe_public_url("http://127.0.0.1/secret") is False
    assert is_safe_public_url("https://evil.example/x") is False
    try:
        scrape_public_page("http://localhost/admin")
        assert False, "should block"
    except ValueError:
        pass


def test_scrape_uses_injected_http_on_allowlisted_host():
    http = FakeHttp(text_by_url={"wikipedia.org": "Karma\nKarma is action."})
    page = scrape_public_page("https://en.wikipedia.org/wiki/Karma", http=http)
    assert page["engine"] in ("httpx", "scrapling")
    assert page["source"] == "public"
    assert "Karma" in page["title"]


def test_catalog_lists_public_api_sources():
    ids = {item["id"] for item in catalog()}
    assert {"gita", "wikipedia", "dictionary", "sunrise", "open_library", "youtube_oembed"} <= ids


def test_dictionary_word_maps_hindi():
    assert dictionary_word("ध्यान कैसे करें") == "meditation"
    assert dictionary_word("karma yoga") == "karma"
