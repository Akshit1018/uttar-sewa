"""Grounded ask pipeline: retrieve → grade → extractive answer → cite.

This is a LangGraph-style node graph without requiring the LangGraph package
at runtime. Every sentence of the answer is copied from retrieved corpus text.
Unrelated questions are refused instead of inventing a teaching.
"""

from typing import Any, Dict, List, Optional

from .relevance_search import expand_query, library_as_qa, rank_answers
from .timestamp_urls import build_watch_url, format_timestamp_display

REFUSE_THRESHOLD = 0.42

REFUSE_TEXT = {
    "hi": "इस विषय पर संकलित प्रवचनों में स्पष्ट उत्तर नहीं मिला। निकटतम क्लिप नीचे हैं — बिना प्रमाण के कोई उपाय नहीं बताया गया।",
    "en": "The collected discourses do not contain a clear answer to this. Nearest clips are below — no remedy was invented.",
}


def _clip_from(item: Dict[str, Any]) -> Dict[str, Any]:
    video_id = item.get("video_id") or ""
    start = float(item.get("start_time") or 0)
    end = float(item.get("end_time") or start)
    kind = "video" if video_id else "curated"
    return {
        "video_id": video_id,
        "video_title": item.get("video_title") or ("Curated teaching" if kind == "curated" else "Spiritual discourse"),
        "start_time": start,
        "end_time": end,
        "formatted_start_time": format_timestamp_display(start) if video_id else None,
        "timestamp_url": build_watch_url(video_id, start) if video_id else "",
        "youtube_url": f"https://www.youtube.com/watch?v={video_id}" if video_id else "",
        "citation_kind": kind,
        "source_question": item.get("question") or "",
        "source_answer": item.get("answer") or "",
        "confidence_score": float(item.get("confidence_score") or 0),
        "channel_id": item.get("channel_id"),
        "channel_name": item.get("channel_name"),
    }


def _node_expand(state: Dict[str, Any]) -> Dict[str, Any]:
    state["expanded_query"] = expand_query(state.get("question") or "", state.get("conversation_history") or [])
    return state


def _node_retrieve(state: Dict[str, Any]) -> Dict[str, Any]:
    corpus = state.get("corpus") or library_as_qa()
    state["ranked"] = rank_answers(
        state["expanded_query"],
        corpus,
        limit=max(3, int(state.get("limit") or 3)),
        channel_id=state.get("channel_id"),
    )
    return state


def _node_grade(state: Dict[str, Any]) -> Dict[str, Any]:
    ranked = state.get("ranked") or []
    top_score = float(ranked[0]["confidence_score"]) if ranked else 0.0
    state["refused"] = (not ranked) or top_score < REFUSE_THRESHOLD
    state["top_score"] = top_score
    return state


def _node_generate(state: Dict[str, Any]) -> Dict[str, Any]:
    language = state.get("language") or "hi"
    ranked = state.get("ranked") or []
    if state.get("refused"):
        state["answer"] = REFUSE_TEXT.get(language) or REFUSE_TEXT["en"]
        return state
    top = ranked[0]
    state["answer"] = (top.get("answer") or "").strip()
    return state


def _node_verify(state: Dict[str, Any]) -> Dict[str, Any]:
    ranked = state.get("ranked") or []
    clips = [_clip_from(item) for item in ranked[:3]]
    state["clips"] = clips
    if not state.get("refused"):
        answer = state.get("answer") or ""
        source_text = " ".join(item.get("answer") or "" for item in ranked[:2])
        if answer and answer not in source_text:
            state["refused"] = True
            language = state.get("language") or "hi"
            state["answer"] = REFUSE_TEXT.get(language) or REFUSE_TEXT["en"]
    return state


def run_ask_graph(state: Dict[str, Any]) -> Dict[str, Any]:
    """LangGraph-style linear graph: expand → retrieve → grade → generate → verify."""
    for node in (_node_expand, _node_retrieve, _node_grade, _node_generate, _node_verify):
        state = node(state)
    return state


def grounded_ask(
    question: str,
    corpus: Optional[List[Dict[str, Any]]] = None,
    conversation_history: Optional[List[str]] = None,
    language: str = "hi",
    limit: int = 3,
    channel_id: Optional[str] = None,
) -> Dict[str, Any]:
    state = run_ask_graph({
        "question": question or "",
        "corpus": corpus if corpus is not None else library_as_qa(),
        "conversation_history": conversation_history or [],
        "language": language if language in ("hi", "en") else "hi",
        "limit": limit,
        "channel_id": channel_id,
    })
    return {
        "answer": state.get("answer") or "",
        "refused": bool(state.get("refused")),
        "clips": state.get("clips") or [],
        "expanded_query": state.get("expanded_query") or question,
        "top_score": float(state.get("top_score") or 0),
    }
