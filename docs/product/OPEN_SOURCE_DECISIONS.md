# Open-source decisions

| Candidate | Class | Why |
|---|---|---|
| LangGraph / extra agent runtime | **REJECT** | Ask graph is already a linear extractive pipeline |
| Vector DB / hybrid search libraries | **REJECT** (for now) | No faithfulness evals; would repeat ultra-search theater |
| New YouTube scraper | **REJECT** | Existing ingest + captions/Whisper path is the product |
| New analytics SDK | **REJECT** | Current events are local; adding a vendor does not fix measurement |

No new runtime dependencies were added in this Green Team pass.
