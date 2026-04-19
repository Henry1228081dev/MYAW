# ??????? Temporal Research & Comparison SOP

## ???? Goal
Ensure all research is time-relevant for 2026 and comparisons use current frontier models.

## ??????? Execution Protocol

1.  **Time-Sync (Mandatory)**: Before searching, verify the current date. If it's April 2026, act like it. Do not use 2024/2025 data as current.
2.  **Tool Selection**:
    *   **Tavily (Deep Research)**: Use this for model comparisons, benchmarks, and complex inquiries. It is your primary "intelligent" search.
    *   **DuckDuckGo (Quick Check)**: Use this for basic facts or if Tavily is overkill.
    *   **Playwright (Extraction)**: Use this to scrape specific technical docs if search snippets aren't enough.
3.  **Model Benchmarking**:
    *   Read `.hermes/MYAW/directives/MODELS.md` for the current SOTA list.
    *   If comparing a new model (e.g., "Coin 3.6"), research its "GPT-Equivalent" tier first.
4.  **Self-Healing**:
    *   If Tavily hits an API limit or error, switch to `ddg_search` immediately.
    *   If a link is dead, do not complain. Find an archive link or a different source.

## ???? Definition of Done (DoD)
- The report references 2026-era models (GPT 5.4, Gemini 3.1, etc.).
- There are no disclaimers about "my knowledge cutoff."
- The tone is arrogant but technically flawless.

