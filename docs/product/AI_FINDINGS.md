# AI findings

Treat AI as guilty. What this product actually does:

## What is honest

- `grounded_ask`: copy top corpus answer or refuse below 0.42. No invented teaching in that path.
- Ingest persist: `segments_to_qa` only (as of TASK-001). Gemini extract is **not** written to corpus.

## HIGH / MEDIUM

### AI-01 — `/search` can still invoke an LLM
**WHAT IS WRONG:** Chat was fixed to `/ask`. Search still goes through `enhanced_search_coordinator` (`ultra` / `intelligent` / `llm` / `hybrid`). User query can leave the box.  
**EVIDENCE:** `server.py` search handler; `enhanced_search_coordinator.py:30-40`, `llm_service.py`.  
**USER IMPACT:** Search may paraphrase or invent while Chat refuses — trust fracture.  
**SEVERITY:** HIGH  
**CONFIDENCE:** HIGH  
**EXPECTED:** Search is lexical rank only, same refuse policy, or labeled “experimental LLM rank”.  
**TEST:** Search with no API keys still deterministic; with keys, assert no invented sentences in `answer` fields.

### AI-02 — No evaluation harness
No fixture set for refuse, faithfulness, Hindi/English, adversarial history.  
**SEVERITY:** HIGH (quality unknown)  
**CONFIDENCE:** CONFIRMED  

### AI-03 — Extractive “questions” are first 80 chars of the caption
**EVIDENCE:** `transcript_ingest.segments_to_qa`.  
**USER IMPACT:** Search is keyword-lucky. “मन भटकता है तो क्या करें?” may miss a caption that answers it in other words.  
**SEVERITY:** HIGH (product)  
**CONFIDENCE:** CONFIRMED  
**COMPETITOR:** [GitaGPT / Chroma RAG](https://github.com/aprameyak/GitaGPT) uses embeddings over a closed corpus.  
**EXPECTED:** Hybrid lexical + embeddings **after** an eval set; still no invented answers.

### AI-04 — Refuse threshold 0.42 is magic
**EVIDENCE:** `grounded_ask.py` `REFUSE_THRESHOLD`. Untuned, no dataset.  
**SEVERITY:** MEDIUM  

### AI-05 — Conversation history is a ranking injection surface
**EVIDENCE:** `expand_query` concatenates history.  
**SEVERITY:** MEDIUM  

### AI-06 — Companions are live public APIs, not evaluated
Wrong Gita verse / wiki disambiguation can sit next to a true video clip. Cards are labeled — still trust-adjacent.  
**SEVERITY:** MEDIUM  

### AI-07 — Gemini extract still in tree
`llm_service.extract_qa_from_transcript` can be rewired. Logs full response on parse fail (`llm_service.py:273-274`).  
**SEVERITY:** MEDIUM (regression + log leak)  

### AI-08 — Marketing says “AI understands your question”
**EVIDENCE:** `AboutPage.jsx` “AI तकनीक”. Actual ask is extractive copy.  
**SEVERITY:** HIGH as a **trust / contradiction** defect.  
**CONFIDENCE:** CONFIRMED  

### AI-09 — No cost/latency budgets
Search hybrid + companions + scrape can fan out httpx calls per question.  
**SEVERITY:** MEDIUM  
