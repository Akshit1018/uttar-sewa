"""Ensure Mongo collections/indexes exist and seed curated Q&A when empty."""

from backend.db_schema import INDEXES, SETTINGS_DOC_ID
from backend.services.channel_registry import topic_for_tags
from backend.services.control_store import default_settings
from backend.spiritual_qa_content import SPIRITUAL_QA_LIBRARY

_TOPIC_CHANNEL = {
    "bhakti": "bhajanmarg",
    "meditation": "meditation",
    "philosophy": "philosophy",
    "peace": "peace",
}


async def ensure_indexes(db) -> dict:
    created = []
    failed = []
    for collection_name, specs in INDEXES.items():
        collection = db[collection_name]
        for spec in specs:
            keys = spec["keys"] if isinstance(spec, dict) else spec
            unique = bool(spec.get("unique")) if isinstance(spec, dict) else False
            name = spec.get("name") if isinstance(spec, dict) else None
            if not name:
                name = "_".join(f"{field}_{direction}" for field, direction in keys)
            try:
                kwargs = {"name": name, "background": True}
                if unique:
                    kwargs["unique"] = True
                await collection.create_index(keys, **kwargs)
                created.append(name)
            except Exception as error:
                if unique:
                    failed.append({"name": name, "error": str(error)})
                    continue
                try:
                    await collection.create_index(keys, name=name, background=True)
                    created.append(name)
                except Exception as inner:
                    failed.append({"name": name, "error": str(inner)})
    return {"created": created, "failed": failed}


async def seed_if_empty(db) -> dict:
    qa_count = await db.question_answers.count_documents({})
    inserted = 0
    if qa_count == 0:
        docs = []
        for item in SPIRITUAL_QA_LIBRARY:
            tags = item.get("tags") or []
            docs.append(
                {
                    "question": item["question"],
                    "answer": item["answer"],
                    "tags": tags,
                    "confidence_score": item.get("confidence_score", 0.8),
                    "video_id": item.get("video_id") or "",
                    "video_title": item.get("video_title") or "Curated teaching",
                    "start_time": float(item.get("start_time") or 0),
                    "end_time": float(item.get("end_time") or 0),
                    "language": "hi" if any(ord(ch) > 127 for ch in item["question"]) else "en",
                    "channel_id": _TOPIC_CHANNEL.get(topic_for_tags(tags), "philosophy"),
                    "pinned": False,
                    "source": "curated_library",
                }
            )
        if docs:
            await db.question_answers.insert_many(docs)
            inserted = len(docs)

    existing = await db.control_settings.find_one({"_id": SETTINGS_DOC_ID})
    if not existing:
        await db.control_settings.insert_one(default_settings())

    return {"qa_seeded": inserted, "qa_total": qa_count + inserted}


async def bootstrap_database(db) -> dict:
    await ensure_indexes(db)
    seed = await seed_if_empty(db)
    return {"indexes": True, **seed}
