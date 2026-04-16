# Updated Implementation Plan: Gemini Grounding as Search "Father"

This plan upgrades the search strategy to use **Gemini Grounding** as the primary research engine, leveraging its high free-tier limits (up to 1,500 RPD) and native "absolute internet" capabilities.

## User Review Required

> [!IMPORTANT]
> **Grounding Advantages:** Using a Gemini model with "Google Search" enabled is significantly more powerful than raw API calls. It performs multiple searches, selects the best sources, and summarizes facts while citing links.
> 
> [!NOTE]
> **Model Selection:** We will use `gemini-3-flash-preview` (which supports grounding) as the primary engine. `gemini-3.1-flash-lite-preview` will be used as a logic-only fallback if needed, as it currently lacks grounding support.

## Proposed Changes

### Layer 1: Directives (SOPs)

#### [MODIFY] [google_search_sop.md](file:///c:/Users/henry/Desktop/Agentic%20workflows/directives/google_search_sop.md)
- Update "Ideal Search Method": Detail why Grounding > Raw CSE.
- Explain the "Father" methodology: Gemini Research -> Raw Data Fallback -> DDG Safety Net.

---

### Layer 2: Execution (Python Scripts)

#### [MODIFY] [google_search.py](file:///c:/Users/henry/Desktop/Agentic%20workflows/execution/google_search.py)
- **Primary Integration**: Add the `google-genai` library logic to call Gemini with `google_search` tool enabled.
- **Smart Result Parsing**: Extract citations and links from the Gemini Grounding response metadata.
- **Improved Fallbacks**: If Gemini grounding is disabled or errors out, automatically drop down to CSE (100 free) or DuckDuckGo.

---

### Layer 3: Environment

#### [MODIFY] [.env](file:///c:/Users/henry/Desktop/Agentic%20workflows/.env)
- Ensure `GOOGLE_API_KEY` is ready for Gemini API calls.

## Why this is the "Ideal Method" for your Model System

1. **Absolute Internet Access**: Unlike a raw API that just gives snippets, Gemini Grounding reads multiple pages and synthesizes the "Absolute" truth with citations.
2. **SEO Mastery**: By using the model that powers Google Search, your agents get the most relevant context for competition research and keyword analysis.
3. **Daily Volume**: You targeting 800 searches/day is easily achievable with Gemini Flash's 1,500 RPD limit (vs the 100/day hard cap of Custom Search).

## Open Questions

1. **Output Format**: Do you want the agent to receive a **synthesized answer** (with citations) or just the **raw list of links** from Gemini? (I recommend the synthesized answer as it's better for research).
2. **Model Pinning**: Should I hardcode `gemini-3-flash-preview` as the search father, or do you want the script to check a list of models in your `.env`?

## Verification Plan

### Automated Tests
- Run `python execution/google_search.py --query "who is currently leads AI agents space?" --provider gemini`
- Verify that the output contains citations/links and a synthesized summary.
- Verify fallback speed when forcing `--provider ddg`.
