import json
import os
from datetime import datetime


PRIMARY_SOURCE_PATHS = [
    "tmp/upwork/raw_jobs_fresh.json",
]

FALLBACK_SOURCE_PATHS = [
    "tmp/upwork/raw_jobs.json",
    ".tmp/fresh_upwork_jobs.json",
]


def compile_leads():
    lead_sources = []

    source_paths = PRIMARY_SOURCE_PATHS if os.path.exists(PRIMARY_SOURCE_PATHS[0]) else FALLBACK_SOURCE_PATHS

    for path in source_paths:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                jobs = json.load(f)
            lead_sources.extend(jobs)
            print(f"Loaded {len(jobs)} jobs from {path}")

    unique_ids = set()
    unique_jobs = []

    for job in lead_sources:
        jid = (
            job.get("id")
            or job.get("jobId")
            or job.get("uid")
            or job.get("url")
            or job.get("externalLink")
        )
        if jid and jid not in unique_ids:
            unique_ids.add(jid)
            unique_jobs.append(job)

    print(f"Total unique leads compiled: {len(unique_jobs)}")

    now = datetime.now()
    date_str = now.strftime("%d,%m,%y")
    time_str = os.getenv("UPWORK_REPORT_HOUR_OVERRIDE") or now.strftime("%Hhr")

    base_dir = os.path.join("UpworkLeadsReport", "Leads Report", date_str, time_str)
    os.makedirs(base_dir, exist_ok=True)

    report_path = os.path.join(base_dir, "full_raw_leads.md")
    md_content = f"# Full Raw Leads Report - {now.strftime('%Y-%m-%d %H:%M')}\n\n"
    md_content += f"Total leads: {len(unique_jobs)}\n\n"

    for i, job in enumerate(unique_jobs, 1):
        posted = job.get("posted") or job.get("postedOn") or job.get("createdAt", "N/A")
        md_content += f"### {i}. {job.get('title', 'No Title')}\n"
        md_content += f"- **URL:** {job.get('url') or job.get('externalLink')}\n"
        md_content += f"- **Budget:** {job.get('budget', 'N/A')}\n"
        md_content += f"- **Posted:** {posted}\n"
        if job.get("query_hits"):
            md_content += f"- **Query Hits:** {', '.join(job.get('query_hits', []))}\n"
        md_content += (
            f"- **Description:** "
            f"{job.get('description', '').replace(chr(10), ' ').replace(chr(13), ' ')}\n\n"
        )

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    merged_json_path = "tmp/upwork/merged_leads.json"
    with open(merged_json_path, "w", encoding="utf-8") as f:
        json.dump(unique_jobs, f, indent=2, ensure_ascii=False)

    print(f"Report saved to: {report_path}")
    return merged_json_path, base_dir


if __name__ == "__main__":
    compile_leads()
