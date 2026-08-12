"""Lexical relevance ranking with conversation-aware query expansion.

This is the default search path: it does not call an LLM, so it works without
API keys and stays deterministic for tests.
"""

import re
from typing import Any, Dict, Iterable, List, Optional, Set

from .channel_registry import DEFAULT_CHANNELS, get_channel, topic_for_tags
from backend.spiritual_qa_content import SPIRITUAL_QA_LIBRARY

_DEVANAGARI_OR_LATIN = re.compile(r"[\u0900-\u097Fa-zA-Z0-9]+")

STOPWORDS = {
    "the", "a", "an", "is", "of", "to", "in", "and", "or", "on", "for", "with",
    "how", "what", "why", "when", "do", "does", "can", "please", "me", "my",
    "i", "we", "you", "it", "this", "that", "from", "about",
    "का", "की", "के", "क्या", "है", "हैं", "में", "से", "को", "और", "यह", "वह",
    "होता", "होती", "करें", "करना", "करूं", "लिए", "एक",
}

SYNONYMS: Dict[str, Set[str]] = {
    "ध्यान": {"meditation", "dhyan", "meditate", "mindfulness"},
    "meditation": {"ध्यान", "dhyan", "meditate", "mindfulness"},
    "meditate": {"ध्यान", "meditation", "dhyan"},
    "mind": {"मन", "mind", "चित्त"},
    "मन": {"mind", "चित्त"},
    "guru": {"गुरु", "teacher", "master", "guide"},
    "गुरु": {"guru", "teacher", "master"},
    "teacher": {"guru", "गुरु", "master"},
    "भक्ति": {"bhakti", "devotion", "worship"},
    "bhakti": {"भक्ति", "devotion"},
    "devotion": {"भक्ति", "bhakti", "worship"},
    "karma": {"कर्म", "action"},
    "कर्म": {"karma", "action"},
    "मोक्ष": {"moksha", "liberation", "salvation"},
    "moksha": {"मोक्ष", "liberation"},
    "liberation": {"मोक्ष", "moksha", "मुक्ति"},
    "peace": {"शांति", "calm", "शान्ति"},
    "शांति": {"peace", "calm"},
    "जीवन": {"life", "purpose", "meaning"},
    "life": {"जीवन"},
    "अर्थ": {"meaning", "purpose"},
    "meaning": {"अर्थ", "purpose"},
    "purpose": {"अर्थ", "उद्देश्य", "meaning"},
}

_FOLLOW_UP = re.compile(
    r"^(और|फिर|उसके|इसके|why|how|what about|tell me more|more|also|"
    r"क्यों|कैसे|और बताओ|और क्या|explain|please explain)\b",
    re.IGNORECASE,
)

_FOLLOW_UP_SHORT = re.compile(
    r"^(और कैसे\??|क्यों\??|why\??|how\??|more\??|और\??)$",
    re.IGNORECASE,
)


def tokenize(text: str) -> List[str]:
    if not text:
        return []
    return [token.lower() for token in _DEVANAGARI_OR_LATIN.findall(text)]


def _expand_tokens(tokens: Iterable[str]) -> Set[str]:
    expanded: Set[str] = set()
    for token in tokens:
        if token in STOPWORDS:
            continue
        expanded.add(token)
        expanded.update(SYNONYMS.get(token, set()))
    return expanded


def is_follow_up(query: str) -> bool:
    text = (query or "").strip()
    if not text:
        return False
    if _FOLLOW_UP_SHORT.match(text):
        return True
    if len(tokenize(text)) <= 4 and _FOLLOW_UP.match(text):
        return True
    return False


def expand_query(query: str, conversation_history: Optional[List[str]] = None) -> str:
    text = (query or "").strip()
    history = [item.strip() for item in (conversation_history or []) if item and item.strip()]
    if not text:
        return text
    if history and is_follow_up(text):
        prior = " ".join(history[-3:])
        return f"{prior} {text}".strip()
    return text


def _content_tokens(item: Dict[str, Any]) -> Set[str]:
    tags = " ".join(str(tag) for tag in item.get("tags", []))
    blob = f"{item.get('question', '')} {item.get('answer', '')} {tags}"
    return set(tokenize(blob))


def _has_devanagari(text: str) -> bool:
    return bool(re.search(r"[\u0900-\u097F]", text or ""))


def _score(query: str, item: Dict[str, Any]) -> float:
    query_tokens = tokenize(query)
    if not query_tokens:
        return 0.0

    question = (item.get("question") or "").strip()
    query_norm = query.strip().lower()
    question_norm = question.lower()

    if query_norm == question_norm:
        return 1.0
    if query_norm and query_norm in question_norm:
        return 0.96

    query_terms = _expand_tokens(query_tokens)
    content = _content_tokens(item)
    if not query_terms:
        return 0.0

    overlap = query_terms & (content | _expand_tokens(content))
    coverage = len(overlap) / max(1, len(query_terms))

    question_tokens = _expand_tokens(tokenize(question))
    question_overlap = len(query_terms & question_tokens) / max(1, len(query_terms))

    tag_tokens = _expand_tokens(tokenize(" ".join(str(tag) for tag in item.get("tags", []))))
    tag_bonus = 0.12 if query_terms & tag_tokens else 0.0
    script_bonus = 0.08 if _has_devanagari(query) == _has_devanagari(question) else 0.0

    stored_confidence = float(item.get("confidence_score") or 0.5)
    score = (
        (0.55 * question_overlap)
        + (0.25 * coverage)
        + tag_bonus
        + script_bonus
        + (0.10 * stored_confidence)
    )
    return min(0.94, score)


def rank_answers(
    query: str,
    qa_database: List[Dict[str, Any]],
    limit: int = 5,
    channel_id: Optional[str] = None,
) -> List[Dict[str, Any]]:
    text = (query or "").strip()
    if not text:
        return []

    corpus = list(qa_database or [])
    if channel_id and channel_id not in ("all", ""):
        channel = get_channel(channel_id)
        topic = channel["topic"] if channel else channel_id
        filtered = [
            item for item in corpus
            if item.get("channel_id") in {channel_id, topic}
            or topic_for_tags(item.get("tags", [])) == topic
        ]
        if filtered:
            corpus = filtered

    scored: List[Dict[str, Any]] = []
    query_norm = text.lower()
    for item in corpus:
        score = _score(text, item)
        if score < 0.18:
            continue
        ranked = dict(item)
        ranked["confidence_score"] = round(score, 4)
        question_norm = (item.get("question") or "").strip().lower()
        ranked["_exact"] = 1 if query_norm == question_norm else 0
        scored.append(ranked)

    scored.sort(key=lambda item: (item["_exact"], item["confidence_score"]), reverse=True)
    for item in scored:
        item.pop("_exact", None)
    return scored[: max(1, limit)]


def related_questions(
    current: Dict[str, Any],
    qa_database: List[Dict[str, Any]],
    limit: int = 3,
) -> List[str]:
    current_question = (current.get("question") or "").strip()
    tags = {str(tag).lower() for tag in current.get("tags", [])}
    candidates: List[str] = []
    for item in qa_database:
        question = (item.get("question") or "").strip()
        if not question or question == current_question:
            continue
        item_tags = {str(tag).lower() for tag in item.get("tags", [])}
        if tags and tags & item_tags:
            candidates.append(question)
        if len(candidates) >= limit:
            break
    if len(candidates) < limit:
        for item in qa_database:
            question = (item.get("question") or "").strip()
            if question and question != current_question and question not in candidates:
                candidates.append(question)
            if len(candidates) >= limit:
                break
    return candidates[:limit]


def library_as_qa() -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []
    for qa in SPIRITUAL_QA_LIBRARY:
        topic = topic_for_tags(qa.get("tags", []))
        channel = next((entry for entry in DEFAULT_CHANNELS if entry["topic"] == topic), None)
        items.append({
            "question": qa["question"],
            "answer": qa["answer"],
            "tags": qa.get("tags", []),
            "confidence_score": qa.get("confidence_score", 0.8),
            "video_id": "",
            "start_time": 0.0,
            "end_time": 60.0,
            "video_title": "Curated teaching",
            "channel_id": channel["id"] if channel else topic,
            "channel_name": channel["name"] if channel else topic,
            "language": "hi" if _has_devanagari(qa["question"]) else "en",
        })
    return items


def recommend_from_history(
    recent_queries: Optional[List[str]],
    qa_database: List[Dict[str, Any]],
    limit: int = 6,
    channel_id: Optional[str] = None,
) -> List[Dict[str, Any]]:
    combined = " ".join(query.strip() for query in (recent_queries or []) if query and query.strip())
    if not combined:
        combined = "भक्ति ध्यान शांति karma meditation"
    return rank_answers(combined, qa_database, limit=limit, channel_id=channel_id)
