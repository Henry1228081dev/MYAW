# Upwork Job Scrape & Apply Pipeline

Scrape Upwork jobs matching AI/automation keywords, score them using Gemini 3 Flash, and generate high-conversion proposals for the top-ranked leads.

## 30-Minute Freshness Policy

**CRITICAL:** Only jobs posted within the last 30 minutes are considered valid leads.

Priority freshness rules:

- Ideal target: jobs posted in the last 3 minutes
- Acceptable upper bound: jobs posted in the last 30 minutes
- Anything older than 30 minutes should be rejected from the active apply pool

Proposal-count rules:

- Ideal target: jobs with fewer than 5 proposals/applicants
- If proposal count is available, reject jobs with 5 or more proposals from the active apply pool
- If proposal count is unavailable, the job may remain in the pool but must be ranked below jobs with confirmed low competition

## Phase 1: Scrape & Filter (Python)

Fetch raw jobs from Apify. Perform initial keyword filtering to remove noise.

### Phase 1A: Multi-Query Search Batches

Do not scrape one broad random pool and filter it later. Run multiple narrow searches for automation-native buyer intent, then merge and dedupe the results before any AI scoring.

Use small targeted query clusters first:

- `n8n automation`
- `zapier automation`
- `make.com automationo`
- `api integration`
- `webhook automation`
- `openai automation`
- `python automation`
- `ai agent workflow`
- `crm automation`
- `hubspot automation`
- `airtable automation`
- `google sheets automation`
- `lead generation automation`
- `lead enrichment automation`
- `cold email automation`
- `apollo lead scraping`
- `instantly automation`
- `gmail automation`
- `slack webhook automation`
- `modal webhook`
- `pdf extraction automation`
- `vapi voice ai`
- `lead routing automation`

Execution rules:

- Start with 10-20 results per query cluster, not one 200-job blast
- Merge all query batches into one candidate pool
- Dedupe by job URL / job ID before any further filtering
- Keep the query keyword that found each job for later reporting
- If a query cluster produces repeated junk, reduce or remove it in the next run
- Prefer query results that are very fresh and low competition over broader volume

### Phase 1B: Apify Cost Control

Use the cheapest practical Apify approach and treat the $5 free credit as a hard budget cap.

Cost rules:

- Prefer pay-per-result Upwork job actors over monthly-subscription actors
- Keep each actor run small and targeted; avoid large broad runs
- Default first pass: 10-20 jobs per query cluster
- Hard cap one full pipeline run at 200 raw jobs merged across all clusters
- Stop early if enough valid automation leads are found before the cap
- Reuse one fresh merged pool for scoring instead of re-running the actor multiple times in the same session
- Do not use premium proxy-heavy scraping setups unless the cheap actor path is clearly failing

### Phase 1C: Deterministic Relevance Filter

Before any Gemini scoring, apply local rule-based filtering. AI should never read obvious junk.

Strong positive signals:

- `n8n`
- `zapier`
- `make.com`
- `automation`
- `api integration`
- `webhook`
- `openai`
- `python`
- `ai agent`
- `crm automation`
- `hubspot automation`
- `airtable`
- `google sheets automation`
- `lead generation`
- `lead enrichment`
- `cold email automation`
- `apollo`
- `instantly`
- `gmail automation`
- `slack webhook`
- `modal`
- `pdf extraction`
- `lead routing`
- `voice ai`

Weak positive signals:

- `ai`
- `workflow`
- `integration`
- `chatbot`
- `python`

Negative signals:

- `ui/ux`
- `figma`
- `graphic design`
- `video editor`
- `copywriter`
- `virtual assistant`
- `customer support`
- `bookkeeper`
- `seo specialist`
- `full stack tech lead`
- `cto`
- `social media`
- `newsletter`

Filter rules:

- A job must match at least one strong positive signal in title, description, or skills
- Weak positives alone are not enough
- Reject jobs with dominant negative-signal intent even if they mention AI once
- Reject jobs older than 30 minutes
- Strongly prefer jobs posted in the last 3 minutes
- If proposals/applicants count is available, reject jobs with 5 or more proposals
- If proposals/applicants count is unavailable, allow the job but score it below confirmed low-proposal jobs

### Phase 1D: Hidden Gem Prefilter

After deterministic relevance filtering, rank for winnability before AI scoring.

Prefer:

- Non-featured jobs
- Lower connect cost
- Payment-verified clients
- Posted in the last 3 minutes
- Fewer than 5 proposals/applicants
- Clear, narrow operational scope
- Real business workflow pain
- Fixed-price or tightly bounded hourly jobs
- Jobs that can plausibly be solved by one automation specialist

Penalize:

- Featured/promoted jobs
- Jobs older than 30 minutes
- Jobs with 5 or more proposals/applicants
- Vague `AI expert needed` posts
- Giant broad platform rebuilds
- Team-lead / CTO / management roles
- Generic full-stack jobs with incidental AI mentions
- Jobs where automation is optional rather than the core deliverable

## Phase 2: AI Scoring & Ranking (Gemini 3 Flash)

**CRITICAL:** Every job must be scored by Gemini 3 Flash before proposal generation.

- **Input:** Job title, description, and budget.
- **Criteria:** Score 1-10 based on "Automation Complexity" and "AI Relevance".
- **Action:** Sort all leads by score (descending).

### Phase 2A: AI Scoring Scope

Gemini should only score the shortlist that survives Phase 1 deterministic filtering and hidden-gem prefiltering.

Rules:

- Never send the full raw scrape to Gemini
- Target shortlist size before AI scoring: 25-40 jobs
- If more than 40 jobs survive deterministic filtering, trim by hidden-gem score first
- Only the top-ranked jobs after Gemini scoring move forward

### Phase 2B: Scoring Model Add-On

Gemini scoring should still center on `Automation Complexity` and `AI Relevance`, but include these tie-breakers:

- Scope clarity
- Workflow ownership vs generic dev work
- Business outcome strength
- Winnability for a solo automation specialist
- Client quality

Gemini should penalize:

- Broad management roles
- Generic platform rebuilds
- Jobs with only weak AI relevance
- Jobs where automation is incidental

### Phase 2C: Hidden Gem Score

In addition to Gemini fit scoring, compute a local hidden-gem score to prioritize jobs that are more likely to convert.

Suggested factors:

- `+2` if non-featured
- `+2` if payment verified
- `+2` if connects cost is low relative to similar jobs
- `+2` if scope is narrow and concrete
- `+1` if budget is reasonable for MVP automation work
- `+1` if client has prior hires or spend
- `-2` if featured/promoted
- `-2` if role is leadership-heavy
- `-2` if job is broad/vague
- `-1` if budget is obviously weak for the scope

Final ranking rule:

- Primary sort: Gemini fit score
- Secondary sort: hidden-gem score
- Tertiary sort: freshness

## Phase 3: Top 10 Proposal Generation

**CRITICAL:** Gemini scores and ranks. The orchestrator writes the actual cover letters and proposals.

Proposal authorship rules:

- Gemini may be used for scoring/ranking only
- The orchestrator must read the shortlisted raw lead data and write the final cover letters manually
- The orchestrator must write the final full proposals manually
- Do not delegate proposal writing to Gemini or another model once the shortlist is selected
- Proposal quality is determined by the orchestrator's judgment after reviewing the raw lead details, not by generic model output

Only process the **Top 10 highest-scoring jobs** for:

1. **Contact Discovery:** Extract the client's name.
2. **Cover Letter:** The orchestrator crafts a short (<35 words) high-conversion pitch.
3. **Full Strategy:** The orchestrator writes a 5-step implementation plan.

## Output Paths

Raw and intermediate files:

- Fresh raw query results: `tmp/upwork/raw_jobs_fresh_raw.json`
- Fresh filtered automation pool: `tmp/upwork/raw_jobs_fresh.json`
- Legacy/raw scrape fallback: `tmp/upwork/raw_jobs.json`
- Final merged pool used for ranking: `tmp/upwork/merged_leads.json`
- Legacy report folder to ignore: `tmp/UpworkLeadsReport/`

Report folder structure:

- Root report folder: `UpworkLeadsReport/Leads Report/`
- `tmp/UpworkLeadsReport/` is legacy and should not be used as the active report destination
- Date folder format: `DD,MM,YY`
- Hour folder format: `HHhr`

Navigation example:

- Go to `UpworkLeadsReport/Leads Report/`
- Open today's date folder, for example `26,03,26`
- Open the current hour folder, for example `10hr`
- Inside that folder:
  - `full_raw_leads.md` contains the full raw lead data for review
  - `leads_report.md` contains the ranked leads plus orchestrator-written cover letters and proposals

The final report must be written to the active dated folder, not to an arbitrary standalone path.
The active dated folder always lives under `UpworkLeadsReport/Leads Report/`, not under `tmp/UpworkLeadsReport/`.

## Output: UpworkLeadsReport/Leads Report/DD,MM,YY/HHhr/leads_report.md

The final report must list:

- **Top 10:** Full proposals with copy-pasteable cover letters.
- **The Rest:** A ranked list of remaining leads with scores and brief justifications.

Options:

- `--workers N`: Parallel Opus 4.5 calls (default: 5)
- `--sheet-id ID`: Use existing sheet (creates new if omitted)
- `--filter-keywords "ai,automation"`: Only process jobs matching keywords

For each job:

- Generates Apply Now link (`/nx/proposals/job/{id}/apply/`)
- Stores full raw job details in `full_raw_leads.md` inside the dated hour folder
- Writes personalized cover letters directly in `leads_report.md`
- Writes full proposals directly in `leads_report.md`
- Outputs to new Google Sheet with all columns only if that export is still needed for the run

## Output

Google Sheet with columns:

| Column                       | Description                          |
| ---------------------------- | ------------------------------------ |
| Keyword                      | Search term that found this job      |
| Title                        | Job title                            |
| URL                          | Job listing URL                      |
| Budget                       | Fixed price or hourly range          |
| Experience                   | Required level                       |
| Skills                       | Top 5 required skills                |
| Client Country               | Client location                      |
| Client Spent                 | Total $ spent on platform            |
| Client Hires                 | Total past hires                     |
| Connects                     | Cost to apply                        |
| Posted                       | Date posted                          |
| **Contact Name**       | Discovered first name (if found)     |
| **Contact Confidence** | high/medium/low - how certain we are |
| **Apply Link**         | One-click apply URL                  |
| **Cover Letter**       | Personalized pitch                   |
| **Proposal Doc**       | Google Doc with full proposal        |

## Cover Letter Format

Must stay above the fold (~35 words max). Uses short paraphrases:

```
Hi. I work with [2-4 word paraphrase] daily & just built a [2-5 word thing]. Free walkthrough: [PROPOSAL_DOC_LINK]
```

Example:

> Hi. I work with n8n automations daily & just built an AI lead scoring pipeline. Free walkthrough: https://docs.google.com/document/d/...

## Proposal Format

Conversational, first-person format written as Nick:

```
Hey [name if available].

I spent ~15 minutes putting this together for you. In short, it's how I would create your [paraphrasedThing] system end to end.

I have a lot of experience designing and building similar workflows at scale.

Here's a step-by-step, along with my reasoning at every point:

My proposed approach

[4-6 numbered steps with reasoning for each]

What you'll get

[2-3 concrete deliverables]

Timeline

[Realistic estimate, conversational tone]
```

Tone: Direct, confident, peer-to-peer. Not salesy or formal.

## Keywords for AI/Automation

| Keyword         | Target Jobs                        |
| --------------- | ---------------------------------- |
| automation      | Workflow automation, Zapier/Make   |
| ai agent        | AI assistants, autonomous systems  |
| n8n             | Self-hosted automation             |
| python          | Custom scripts, backend automation |
| gpt             | OpenAI API, LLM apps               |
| workflow        | Business process, systems          |
| api integration | Connect services, middleware       |
| scraping        | Data extraction, lead gen          |
| ai consultant   | Strategy, implementation           |

## Edge Cases

- **No jobs found**: Increase limit or broaden keywords
- **Anthropic rate limit**: Reduce `--workers` to 2-3
- **Google Doc creation fails**: Script retries 4x with exponential backoff (1.5s, 3s, 6s, 12s)
- **Google API quota**: Max ~100 doc creates/day on free tier
- **Sheet already has columns**: Use `--sheet-id` to append, or omit for fresh sheet
- **Too many irrelevant jobs**: Tighten query clusters and require at least one strong positive signal before Gemini scoring
- **Too many featured jobs**: Penalize featured jobs in hidden-gem scoring and lower per-query result limits
- **Apify credit burn**: Reduce jobs per query cluster, reuse merged pools, and stop once enough valid leads are found
- **Too few automation-native jobs**: Add adjacent high-intent clusters like `zapier hubspot`, `n8n webhook`, `openai crm`, or `pdf extraction`

## Contact Name Discovery

The system uses Opus 4.5 to discover the likely contact name from each job posting:

1. **From description** (high confidence): Signatures like "Thanks, John" or "I'm Sarah"
2. **From company research** (medium confidence): If a company name is mentioned and AI recognizes it, infers founder/CEO
3. **Hedged greeting**: For medium/low confidence names, proposal uses "Hey [Name] (if I have the right person)"

Contact info is stored in output and displayed in the Google Sheet.

## Learnings

- Apify job actors can support actor-level keyword, category, budget, and client filters; use source filtering before local filtering whenever the actor supports it
- Cheap Apify usage depends on narrow query batching, not broad high-limit scrapes
- Monthly Apify actors are a poor fit while using only a $5 free credit budget; prefer pay-per-result job actors
- The cheapest useful architecture is: targeted fetch -> deterministic filter -> AI scoring -> proposal generation
- Weak keywords like `ai` or `workflow` are not enough on their own; require at least one strong automation signal
- Query clusters should be measured and iterated based on which ones produce real automation jobs
- Job URL format: `https://www.upwork.com/jobs/~{id}` → Apply: `https://www.upwork.com/nx/proposals/job/~{id}/apply/`
- Opus 4.5 model ID: `claude-opus-4-5-20251101`
- Extended thinking budget: 5000 tokens for cover letters, 8000 for proposals
- Parallel Opus calls work well (5 workers), but Google Docs API needs serialization (semaphore)
- Doc creation uses `threading.Semaphore(1)` + retry with exponential backoff to avoid SSL errors
- 10 jobs with 5 workers: ~2 min (vs ~20 min sequential)
- Contact name discovery uses Opus 4.5 before proposal generation
- Don't use regex for name extraction - AI handles edge cases much better

## Run Metrics

Every run should report:

- Raw jobs fetched
- Jobs fetched per query cluster
- Jobs removed by deterministic negative filters
- Jobs surviving the strong-positive filter
- Jobs surviving hidden-gem prefilter
- Jobs sent to Gemini for scoring
- Top 3 query clusters by final lead quality

## Changelog

- [2026-03-26] Added multi-query Stage 1 search batching, deterministic relevance filtering, hidden-gem prefiltering, Gemini shortlist rules, and Apify cost controls for low-credit operation.
- [2026-03-26] Clarified that the orchestrator writes final cover letters and proposals manually, and formalized the dated `UpworkLeadsReport/Leads Report/DD,MM,YY/HHhr/` output structure with `full_raw_leads.md` and `leads_report.md`.
