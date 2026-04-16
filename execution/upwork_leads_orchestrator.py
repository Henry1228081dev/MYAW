import json
import os
import re
import sys
from datetime import datetime

import google.generativeai as genai
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from execution.compile_upwork_leads import compile_leads

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in .env")
genai.configure(api_key=API_KEY)


def local_heuristic_score(job: dict) -> dict:
    text = (
        job.get("title", "") + " " +
        job.get("description", "") + " " +
        " ".join(job.get("skills", []))
    ).lower()
    keywords = [
        "automation", "python", "n8n", "zapier", "make.com", "openai",
        "llm", "agent", "workflow", "api", "webhook", "crm",
        "google sheets", "lead generation", "voice ai", "apollo", "instantly",
    ]
    score = 1
    matched = []
    for keyword in keywords:
        if keyword in text:
            score += 1
            matched.append(keyword)

    return {
        "score": min(score, 10),
        "reason": f"Local heuristic match: {', '.join(matched) if matched else 'generic'}",
    }


def score_job(job: dict) -> dict:
    title = job.get("title", "")
    desc = job.get("description", "")
    skills = job.get("skills", [])
    try:
        model = genai.GenerativeModel("gemini-3-flash-preview")
        prompt = (
            "Rate this Upwork job for Nick, an AI/automation specialist.\n"
            f"TITLE: {title}\n"
            f"DESCRIPTION: {desc[:4000]}\n"
            f"SKILLS: {skills}\n\n"
            "Score 1-10 based on automation complexity, AI relevance, scope clarity, "
            "and likelihood that a solo automation specialist can win it.\n"
            'Return ONLY JSON: {"score": 1-10, "reason": "Short 1-sentence why"}'
        )
        response = model.generate_content(prompt)
        text = response.text.strip()
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        return json.loads(text)
    except Exception:
        return local_heuristic_score(job)


def discover_contact_name(job: dict) -> dict:
    try:
        model = genai.GenerativeModel("gemini-3-flash-preview")
        prompt = (
            f"Find first name only from this Upwork job: {job.get('description', '')[:3000]}. "
            'Return ONLY JSON: {"name": "FirstName", "confidence": "high/med/low"}'
        )
        response = model.generate_content(prompt)
        text = response.text.strip()
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        return json.loads(text)
    except Exception:
        return {"name": None, "confidence": "low"}


def parse_budget(job: dict) -> str:
    budget = str(job.get("budget", "Not specified")).strip()
    return budget if budget else "Not specified"


def choose_focus_phrase(job: dict) -> str:
    text = (
        job.get("title", "") + " " +
        job.get("description", "") + " " +
        " ".join(job.get("skills", []))
    ).lower()
    mapping = [
        ("voice ai", "voice AI intake"),
        ("elevenlabs", "voice qualification flows"),
        ("voiceflow", "lead qualification flows"),
        ("slack", "Slack dispatch workflows"),
        ("webhook", "webhook automations"),
        ("google sheets", "Google Sheets automations"),
        ("hubspot", "HubSpot automations"),
        ("crm", "CRM workflows"),
        ("lead generation", "lead routing systems"),
        ("lead enrichment", "lead enrichment pipelines"),
        ("cold email", "outreach automations"),
        ("apollo", "lead data pipelines"),
        ("instantly", "outbound systems"),
        ("pdf", "document extraction workflows"),
        ("api", "API automations"),
        ("n8n", "n8n workflows"),
        ("zapier", "Zapier automations"),
        ("make.com", "Make automations"),
        ("python", "Python automations"),
        ("automation", "automation systems"),
    ]
    for key, phrase in mapping:
        if key in text:
            return phrase
    return "automation systems"


def choose_recent_build(job: dict) -> str:
    text = (
        job.get("title", "") + " " +
        job.get("description", "") + " " +
        " ".join(job.get("skills", []))
    ).lower()
    mapping = [
        ("voice ai", "an AI intake agent"),
        ("hubspot", "a CRM routing workflow"),
        ("crm", "a lead pipeline system"),
        ("google sheets", "a Sheets-driven ops workflow"),
        ("slack", "a Slack alerting workflow"),
        ("webhook", "a webhook-based automation"),
        ("pdf", "a document parsing pipeline"),
        ("lead generation", "a lead qualification workflow"),
        ("zapier", "a multi-step Zapier system"),
        ("n8n", "an n8n automation flow"),
        ("python", "a Python backend workflow"),
    ]
    for key, phrase in mapping:
        if key in text:
            return phrase
    return "a similar automation system"


def extract_deliverables(job: dict) -> list[str]:
    focus = choose_focus_phrase(job)
    return [
        f"A working {focus} build with the core logic implemented end to end",
        "A tested workflow with clear edge-case handling and handoff points",
        "Clean documentation so the system is easy to extend after launch",
    ]


def estimate_timeline(job: dict) -> str:
    text = (
        job.get("title", "") + " " +
        job.get("description", "")
    ).lower()
    if "mvp" in text or "simple" in text:
        return "I would scope this as a lean MVP first. Realistically, I can get the first working version in a few days, then use a short hardening pass for edge cases and cleanup."
    if "long-term" in text:
        return "I would split this into a first cleanup/build phase, then keep improving it in short iterations once the core workflow is stable."
    return "I would start with the highest-value workflow first, get that live quickly, then do a second pass for testing, polish, and the non-critical edge cases."


def build_cover_letter(job: dict) -> str:
    need = choose_focus_phrase(job)
    recent_build = choose_recent_build(job)
    return f"Hi. I work with {need} daily & just built {recent_build}. Happy to walk you through it."


def build_step_lines(job: dict) -> list[str]:
    text = (
        job.get("title", "") + " " +
        job.get("description", "")
    ).lower()

    steps = [
        "1. I would map the current workflow first so the automation is built around the real handoff points, data sources, and failure cases rather than assumptions.",
        "2. I would build the core flow end to end with the right triggers, transformations, and routing logic so the system actually removes manual work instead of just moving it around.",
        "3. I would add the integrations next and validate the data contract at each step so records stay clean and actions stay predictable.",
        "4. I would add safeguards for duplicates, bad inputs, retries, and exception handling because that is usually where these systems break in production.",
        "5. I would finish with testing, tuning, and documentation so you have something stable that can be extended without rewriting it later.",
    ]

    if "voice" in text or "elevenlabs" in text or "voiceflow" in text:
        steps[1] = "2. I would build the qualification flow around the actual caller journey so the bot asks the right questions, routes correctly, and hands off only the qualified cases."
        steps[2] = "3. I would wire the voice stack, calendar handoff, and any CRM or notification tools together so the whole intake path is reliable from first interaction to booked call."
    elif "crm" in text or "hubspot" in text or "gohighlevel" in text or "ringy" in text:
        steps[1] = "2. I would clean up the core pipeline logic first so lead intake, tagging, stage movement, and follow-up actions behave consistently."
        steps[2] = "3. I would connect the CRM automations to the right triggers, templates, and status updates so the team can trust the workflow day to day."
    elif "google sheets" in text:
        steps[2] = "3. I would structure the Sheets layer carefully so the automation has a stable source of truth instead of brittle cell-by-cell logic."

    return steps


def build_proposal(job: dict, contact_info: dict | None = None) -> str:
    name = (contact_info or {}).get("name")
    confidence = (contact_info or {}).get("confidence", "low")
    if name and confidence == "high":
        greeting = f"Hey {name}."
    elif name:
        greeting = f"Hey {name} (if I have the right person)."
    else:
        greeting = "Hey."

    focus = choose_focus_phrase(job)
    deliverables = extract_deliverables(job)
    timeline = estimate_timeline(job)
    step_lines = build_step_lines(job)

    lines = [
        greeting,
        "",
        f"I spent ~15 minutes putting this together for you. In short, it's how I would create your {focus} system end to end.",
        "",
        "I do a lot of work in this exact area, especially where the hard part is not the tool itself but getting the workflow, integrations, and exception handling right.",
        "",
        "Here's a step-by-step, along with my reasoning at every point:",
        "",
        "My proposed approach",
        "",
    ]
    lines.extend(step_lines)
    lines.extend(
        [
            "",
            "What you'll get",
            "",
            f"- {deliverables[0]}",
            f"- {deliverables[1]}",
            f"- {deliverables[2]}",
            "",
            "Timeline",
            "",
            timeline,
        ]
    )
    return "\n".join(lines)


def orchestrate():
    print("Step 1: Compiling leads...")
    merged_json_path, base_dir = compile_leads()

    with open(merged_json_path, "r", encoding="utf-8") as f:
        jobs = json.load(f)

    print(f"Step 2: Ranking all {len(jobs)} leads...")
    scored_jobs = []
    for i, job in enumerate(jobs[:60], 1):
        safe_title = job.get("title", "")[:60].encode("ascii", "ignore").decode()
        print(f"  [{i}/{min(len(jobs), 60)}] Scoring: {safe_title}...")
        score_res = score_job(job)
        job["fit_score"] = score_res.get("score", 0)
        job["score_reason"] = score_res.get("reason", "")
        scored_jobs.append(job)

    ranked_jobs = sorted(scored_jobs, key=lambda x: x.get("fit_score", 0), reverse=True)
    top_10 = ranked_jobs[:10]
    remaining = ranked_jobs[10:]

    print("Step 3: Writing orchestrator proposals for TOP 10...")
    for i, job in enumerate(top_10, 1):
        safe_title = job.get("title", "")[:60].encode("ascii", "ignore").decode()
        print(f"  [{i}/10] Writing: {safe_title}...")
        contact = discover_contact_name(job)
        job["contact_name"] = contact.get("name")
        job["contact_confidence"] = contact.get("confidence")
        job["cover_letter"] = build_cover_letter(job)
        job["proposal_doc_text"] = build_proposal(job, contact)

    now = datetime.now()
    report_path = os.path.join(base_dir, "leads_report.md")

    md = f"# Scored Upwork Leads Report - {now.strftime('%Y-%m-%d %H:%M')}\n\n"
    md += "## TOP 10 PROPOSALS\n\n"

    for job in top_10:
        md += f"### {job.get('title')}\n"
        md += f"- **Score:** {job.get('fit_score')}/10 - {job.get('score_reason')}\n"
        md += f"- **URL:** {job.get('url') or job.get('externalLink')}\n"
        md += f"- **Budget:** {parse_budget(job)}\n"
        md += f"- **Posted:** {job.get('posted') or job.get('postedOn') or job.get('createdAt', 'N/A')}\n"
        if job.get("query_hits"):
            md += f"- **Query Hits:** {', '.join(job.get('query_hits', []))}\n"
        md += f"- **Contact Name:** {job.get('contact_name') or 'N/A'}\n\n"
        md += f"#### Cover Letter\n```\n{job.get('cover_letter')}\n```\n\n"
        md += f"#### Strategy\n{job.get('proposal_doc_text')}\n\n---\n\n"

    md += "## REMAINING RANKED LEADS\n\n"
    for job in remaining:
        md += f"- **{job.get('fit_score')}/10**: {job.get('title')} - [Link]({job.get('url') or job.get('externalLink')})\n"
        md += f"  - *Reason:* {job.get('score_reason')}\n\n"

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"\nFinal report saved to: {report_path}")


if __name__ == "__main__":
    orchestrate()
