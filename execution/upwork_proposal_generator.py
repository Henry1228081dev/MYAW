#!/usr/bin/env python3
"""
Upwork Proposal Generator (Gemini 3 Flash - Advanced Ranking Version)

Grabs full job data, scores it using Gemini 3 Flash, ranks the leads, 
and generates full deep-dive proposals for the top 3.
"""

import os
import json
import argparse
import time
import google.generativeai as genai
from datetime import datetime
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

# Configure Gemini - Strictly from environment
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    print("Error: GOOGLE_API_KEY not found in .env file.")
    exit(1)

genai.configure(api_key=API_KEY)

def score_job(job: dict) -> dict:
    """Use Gemini 3 Flash to rate a job's fit (1-10)."""
    title = job.get('title', '')
    desc = job.get('description', '')
    skills = job.get('skills', [])
    
    try:
        model = genai.GenerativeModel("gemini-3-flash-preview")
        prompt = (
            f"Rate this Upwork job for a 'Nick', an AI/Automation expert.\n"
            f"TITLE: {title}\n"
            f"DESCRIPTION: {desc[:1000]}\n"
            f"SKILLS: {skills}\n\n"
            f"Return ONLY JSON: {{\"score\": 1-10, \"reason\": \"Short 1-sentence why\"}}"
        )
        response = model.generate_content(prompt)
        text = response.text.strip()
        if "```json" in text: text = text.split("```json")[1].split("```")[0].strip()
        return json.loads(text)
    except:
        return {"score": 1, "reason": "Error scoring"}

def discover_contact_name(job: dict) -> dict:
    """Use Gemini 3 Flash to find the poster's first name."""
    try:
        model = genai.GenerativeModel("gemini-3-flash-preview")
        prompt = f"Find first name only from this Upwork job: {job.get('description', '')[:1000]}. Return ONLY JSON: {{\"name\": \"FirstName\", \"confidence\": \"high/med/low\"}}"
        response = model.generate_content(prompt)
        text = response.text.strip()
        if "```json" in text: text = text.split("```json")[1].split("```")[0].strip()
        return json.loads(text)
    except:
        return {"name": None, "confidence": "low"}

def generate_cover_letter(job: dict) -> str:
    """Generate high-conversion cover letter (<35 words)."""
    model = genai.GenerativeModel("gemini-3-flash-preview")
    prompt = f"Craft an Upwork cover letter for: {job['title']}. Format: 'Hi. I work with [need] daily & just built [thing]. Happy to walk you through it.' Rules: Conversational, under 35 words. Return ONLY the text."
    response = model.generate_content(prompt)
    return response.text.strip()

def generate_proposal(job: dict, contact_info: dict = None) -> str:
    """Generate 5-step technical implementation strategy."""
    name = contact_info.get("name") if contact_info else None
    greeting = f"Hey {name}" if name else "Hey"
    
    model = genai.GenerativeModel("gemini-3-flash-preview")
    prompt = (
        f"Write an Upwork proposal for: {job['title']}. Start with '{greeting}. I spent ~15 mins on this...'. "
        f"Include 'My proposed approach' with 5 numbered technical steps (WHAT and WHY) and a 'Timeline'. "
        f"Tone: Technical, peer-to-peer. Plain text only."
    )
    response = model.generate_content(prompt)
    return response.text.strip()

def save_advanced_report(top_3: list[dict], ranked_list: list[dict]):
    """Save a ranked and scored report to UpworkLeadsReport/leads_report_YYYY-MM-DD_HH-MM.md."""
    now = datetime.now()
    timestamp_str = now.strftime("%Y-%m-%d_%H-%M")
    timestamp_readable = now.strftime("%Y-%m-%d %H:%M")
    
    md = f"# Upwork Leads Report (Ranked) - {timestamp_readable}\n\n"
    
    # ... (rest of function remains the same)
    
    os.makedirs("UpworkLeadsReport", exist_ok=True)
    report_path = f"UpworkLeadsReport/leads_report_{timestamp_str}.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"Advanced report successfully saved to {report_path}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", required=True)
    args = parser.parse_args()

    with open(args.input) as f:
        jobs = json.load(f)

    # STEP 1: Scoring phase (Limit to top 15 candidates to save quota)
    # We will score 15, then pick top 3 for full generation.
    candidates = jobs[:15]
    print(f"Scoring {len(candidates)} candidates with Gemini 3 Flash...")
    
    for job in candidates:
        print(f"  - Scoring: {job['title'][:50]}...")
        result = score_job(job)
        job['fit_score'] = result.get('score', 0)
        job['score_reason'] = result.get('reason', '')
        time.sleep(12) # Quota protection

    # STEP 2: Sort by score
    sorted_jobs = sorted(candidates, key=lambda x: x.get('fit_score', 0), reverse=True)
    
    top_3 = sorted_jobs[:3]
    remaining = sorted_jobs[3:]

    # STEP 3: Full generation for top 3
    print(f"Generating full proposals for TOP 3 leads...")
    for job in top_3:
        print(f"  - Processing: {job['title'][:50]}...")
        contact = discover_contact_name(job)
        time.sleep(12)
        job['contact_name'] = contact.get('name')
        job['cover_letter'] = generate_cover_letter(job)
        time.sleep(12)
        job['proposal_doc'] = generate_proposal(job, contact)
        time.sleep(12)

    save_advanced_report(top_3, remaining)
    
    # Save raw data to tmp
    with open("tmp/latest_upwork_leads.json", "w") as f:
        json.dump(sorted_jobs, f, indent=2)

if __name__ == "__main__":
    main()
