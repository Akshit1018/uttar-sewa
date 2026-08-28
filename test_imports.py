#!/usr/bin/env python3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

try:
    from backend.models import VideoModel, SearchQuery
    print("Successfully imported VideoModel from backend.models")
    print(
        "SearchQuery includes conversation_history:",
        "conversation_history" in SearchQuery.model_fields,
    )
except Exception as error:
    print(f"Error importing models: {error}")

try:
    from backend.services.processing_service import ProcessingService
    print("Successfully imported ProcessingService")
except Exception as error:
    print(f"Error importing ProcessingService: {error}")

try:
    from backend.services.relevance_search import rank_answers, expand_query
    print("Successfully imported relevance_search")
    print("Follow-up expansion:", expand_query("why?", ["What is karma?"]))
except Exception as error:
    print(f"Error importing relevance_search: {error}")
