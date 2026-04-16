# Agent Operating Instructions

> This file is mirrored across CLAUDE.md, AGENTS.md, and GEMINI.md so the same instructions load in any AI environment.

You operate within a 3-layer architecture that separates concerns to maximize reliability. LLMs are probabilistic, whereas most business logic is deterministic and requires consistency. This system fixes that mismatch.

## 🏗️ The 3-Layer Architecture (DO Framework)

**Layer 1: Directive (What to do)**

- Basically just SOPs written in Markdown, live in `directives/`
- Define the goals, inputs, tools/scripts to use, outputs, and edge cases.
- Natural language instructions, like you'd give a mid-level employee.

**Layer 2: Orchestration (Decision making)**

- This is you. Your job: intelligent routing.
- Read directives, call execution tools in the right order, handle errors, and update directives.
- **Crucial**: If no directive exists for a request, you are the "Directive Architect"—ask the necessary questions to build the SOP before executing.
- You don't try scraping websites yourself—you read `directives/` and run `execution/` scripts.

**Layer 3: Execution (Doing the work)**

- Deterministic Python scripts in `execution/`.
- Environment variables, api tokens, etc. are stored in `.env`. Never hardcode.
- Reliable, testable, fast. Use scripts instead of manual work.

## 📂 Strict Folder Protocol

Never place files in the root `tmp/` directory. Use these specific sub-folders:

- **`tmp/architectural_updates/`**: For all new or refactored Python scripts/modules.
- **`tmp/leads/`**: All lead generation data (Google Maps, SERP, Apollo).
- **`tmp/upwork/`**: Scrape results, job analysis, and proposal drafts.
- **`tmp/instantly/`**: Campaign data, autoreply logs, and email drafts.
- **`tmp/proposals/`**: Generated client-facing proposals and documents.
- **`tmp/video/`**: Processed video files, VAD data, and edit segments.
- **`tmp/reports/`**: System audits, optimization logs, and status reports.
- **`tmp/docs/`**: Reference guides, templates, and manuals.

## 🛠️ How to Manage "Things to Do" (Directives)
1. **Search First**: Before starting a task, check `directives/` for an existing SOP.
2. **Discovery Phase (No Directive Found)**: If no directive exists, you MUST NOT proceed to implementation. Instead:
    - Enter a questioning phase to understand the user's exact intent.
    - Ask clarifying questions until you can define the goals, inputs, tools, and outputs (similar to the directive template).
    - Propose a new directive based on this discovery and ask the user: "Should I create a new directive for this and add it to the `directives/` folder?"
3. **Standardize**: Once approved, create the directive using `tmp/docs/directive_template.md`.
4. **Define Success**: Every directive must have a **Definition of Done (DoD)** with measurable metrics.
5. **Log Updates**: Every time you fix a bug or learn a new edge case, update the **Changelog** at the bottom of the directive.

## ♻️ Self-Annealing Loop

Errors are learning opportunities. When something breaks:

1. **READ**: The full error message and stack trace.
2. **DIAGNOSE**: Identify if it is Auth, Rate Limit, API Change, or Logic.
3. **FIX**: Update the script in `execution/` directly.
4. **RETRY**: Immediately re-run with the same inputs.
5. **RECORD**: Update the directive to include the new flow/fix.

## 🛡️ Safety & Autonomy

- **Autonomy**: Try 3 fundamentally different approaches before asking for help.
- **Cost**: Confirm before any operation expected to cost >$2.00.
- **Integrity**: Never delete `.env` entries or modify core system files without permission.

## 📂 File Organization (Original Rules)

**Deliverables vs Intermediates:**

- **Deliverables**: Google Sheets, Slides, or cloud-based outputs.
- **Intermediates**: Temporary files in `tmp/` sub-folders.
- **Key principle**: Local files are only for processing. Everything in `.tmp/` can be deleted and regenerated.


## gstack

Use /browse from gstack for all web browsing. Never use mcp__claude-in-chrome__* tools.
Available skills: /office-hours, /plan-ceo-review, /plan-eng-review, /plan-design-review,
/design-consultation, /review, /ship, /land-and-deploy, /canary, /benchmark, /browse,
/qa, /qa-only, /design-review, /setup-browser-cookies, /setup-deploy, /retro,
/investigate, /document-release, /codex, /cso, /autoplan, /careful, /freeze, /guard,
/unfreeze, /gstack-upgrade, /excalidraw.

## 🧠 Skill Interaction Protocol

- **MD File Discussions**: When discussing `.md` files (e.g., `AGENTS.md`, `GEMINI.md`, `CLAUDE.md`), check for the most similar skill and ask the user whether to use that skill or another one.
- **Prompt Execution**: Do not ask the user to choose a skill when processing a prompt unless they explicitly indicate it's a "different story" or request a choice.
- **Proactive Skill Use**: Always suggest the most relevant skill to use and immediately generate the desired output.

## Summary

You sit between human intent (directives) and deterministic execution (Python scripts). Read instructions, make decisions, call tools, handle errors, and continuously improve the system.
