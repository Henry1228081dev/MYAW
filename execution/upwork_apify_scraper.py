#!/usr/bin/env python3
"""
Upwork Job Scraper using Apify.

Uses the Upwork Vibe actor with actor-level filters first, then applies
deterministic local filtering to keep token costs down downstream.

Usage:
    python execution/upwork_apify_scraper.py --limit 50
    python execution/upwork_apify_scraper.py --limit 100 --min-hourly 30 --experience intermediate,expert
    python execution/upwork_apify_scraper.py --limit 50 --min-fixed 500 --verified-payment --days 7
    python execution/upwork_apify_scraper.py --limit 50 --keyword "automation" -o .tmp/upwork_jobs.json
"""

import os
import json
import time
import argparse
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()


def scrape_upwork_jobs(
    limit: int = 50,
    from_date: str = None,
    to_date: str = None,
    include_keywords: list[str] | None = None,
    exclude_keywords: list[str] | None = None,
    categories: list[str] | None = None,
    payment_verified: bool | None = None,
) -> list[dict]:
    """Scrape Upwork jobs using Apify actor-level filters where available."""

    api_token = os.environ.get("APIFY_API_TOKEN")
    if not api_token:
        raise ValueError("APIFY_API_TOKEN not found in environment")

    actor_id = "upwork-vibe~upwork-scraper"
    run_url = f"https://api.apify.com/v2/acts/{actor_id}/runs?token={api_token}"

    input_data = {"limit": limit}
    if from_date:
        input_data["fromDate"] = from_date
    if to_date:
        input_data["toDate"] = to_date
    if include_keywords:
        input_data["includeKeywords.keywords"] = include_keywords
        input_data["includeKeywords.matchTitle"] = True
        input_data["includeKeywords.matchDescription"] = True
        input_data["includeKeywords.matchSkills"] = True
    if exclude_keywords:
        input_data["excludeKeywords.keywords"] = exclude_keywords
        input_data["excludeKeywords.matchTitle"] = True
        input_data["excludeKeywords.matchDescription"] = True
        input_data["excludeKeywords.matchSkills"] = True
    if categories:
        input_data["jobCategories"] = categories
    if payment_verified is not None:
        input_data["client.paymentMethodVerified"] = payment_verified

    print(f"Scraping Upwork jobs (limit: {limit})")
    if from_date:
        print(f"  From: {from_date}")
    if to_date:
        print(f"  To: {to_date}")

    # Start the actor run
    response = requests.post(run_url, json=input_data, timeout=60)
    if not response.ok:
        raise Exception(f"Failed to start actor: {response.text}")

    run_info = response.json()
    run_id = run_info.get('data', {}).get('id')
    dataset_id = run_info.get('data', {}).get('defaultDatasetId')

    print(f"Run started: {run_id}")

    # Wait for completion
    status_url = f"https://api.apify.com/v2/actor-runs/{run_id}?token={api_token}"

    for i in range(60):  # Max 5 minutes wait
        time.sleep(3)
        status_resp = requests.get(status_url, timeout=30)
        if status_resp.ok:
            status = status_resp.json().get('data', {}).get('status')
            if status == 'SUCCEEDED':
                print("Scraping completed!")
                break
            elif status in ('FAILED', 'ABORTED', 'TIMED-OUT'):
                raise Exception(f"Actor run failed with status: {status}")
            print(f"  Status: {status}...")
        else:
            print(f"  Error checking status: {status_resp.status_code}")

    # Get results
    dataset_url = f"https://api.apify.com/v2/datasets/{dataset_id}/items?token={api_token}"
    results_resp = requests.get(dataset_url, timeout=60)

    if not results_resp.ok:
        raise Exception(f"Failed to fetch results: {results_resp.text}")

    jobs = results_resp.json()
    print(f"Fetched {len(jobs)} jobs from Apify")
    return jobs


def filter_jobs(
    jobs: list[dict],
    keyword: str = None,
    exclude_keyword: str = None,
    min_hourly: float = None,
    max_hourly: float = None,
    min_fixed: float = None,
    max_fixed: float = None,
    experience_levels: list[str] = None,
    verified_payment: bool = False,
    min_client_spent: float = None,
    min_client_hires: int = None,
    max_age_minutes: int = None,
) -> list[dict]:
    """Apply post-scrape filters to jobs."""

    filtered = []
    now = datetime.now()

    for job in jobs:
        # Freshness filter
        if max_age_minutes:
            posted_str = job.get('createdAt', '')
            if posted_str:
                try:
                    # Parse Upwork's date format (e.g., 2026-03-25T10:15:00.000Z)
                    # Apify usually provides ISO format
                    posted_date = datetime.fromisoformat(posted_str.replace('Z', '+00:00')).replace(tzinfo=None)
                    age = now - posted_date
                    if age.total_seconds() > max_age_minutes * 60:
                        continue
                except Exception as e:
                    print(f"Warning: Could not parse date {posted_str}: {e}")

        # Keyword filter (title + description + skills) - supports multiple
        if keyword:
            keywords = [k.strip().lower() for k in keyword.split(',')]
            text = (
                job.get('title', '') + ' ' +
                job.get('description', '') + ' ' +
                ' '.join(job.get('skills', []))
            ).lower()
            if not any(k in text for k in keywords):
                continue

        if exclude_keyword:
            excluded = [k.strip().lower() for k in exclude_keyword.split(',')]
            text = (
                job.get('title', '') + ' ' +
                job.get('description', '') + ' ' +
                ' '.join(job.get('skills', []))
            ).lower()
            if any(k in text for k in excluded):
                continue


        # Budget filters
        budget = job.get('budget', {})
        hourly = budget.get('hourlyRate', {})
        fixed = budget.get('fixedBudget')

        # Hourly rate filter
        if min_hourly or max_hourly:
            hourly_min = hourly.get('min') or 0
            hourly_max = hourly.get('max') or hourly_min
            if hourly_max == 0 and fixed:
                # Fixed price job, skip hourly filter
                pass
            elif hourly_max == 0:
                continue  # No rate specified
            else:
                if min_hourly and hourly_max < min_hourly:
                    continue
                if max_hourly and hourly_min > max_hourly:
                    continue

        # Fixed price filter
        if min_fixed or max_fixed:
            if not fixed:
                continue
            if min_fixed and fixed < min_fixed:
                continue
            if max_fixed and fixed > max_fixed:
                continue

        # Experience level filter
        if experience_levels:
            job_level = job.get('vendor', {}).get('experienceLevel', '').upper()
            level_match = any(
                lvl.upper() in job_level or job_level in lvl.upper()
                for lvl in experience_levels
            )
            if not level_match:
                continue

        # Client filters
        client = job.get('client', {})

        if verified_payment and not client.get('paymentMethodVerified'):
            continue

        if min_client_spent:
            spent = client.get('stats', {}).get('totalSpent', 0)
            if spent < min_client_spent:
                continue

        if min_client_hires:
            hires = client.get('stats', {}).get('totalHires', 0)
            if hires < min_client_hires:
                continue

        filtered.append(job)

    return filtered


def format_job(job: dict) -> dict:
    """Format job data for display/output."""

    budget = job.get('budget', {})
    hourly = budget.get('hourlyRate', {})
    fixed = budget.get('fixedBudget')

    if fixed:
        budget_str = f"${fixed} fixed"
    elif hourly.get('min') or hourly.get('max'):
        h_min = hourly.get('min', 0)
        h_max = hourly.get('max', h_min)
        budget_str = f"${h_min}-${h_max}/hr"
    else:
        budget_str = "Not specified"

    client = job.get('client', {})
    stats = client.get('stats', {})

    return {
        'id': job.get('uid'),
        'title': job.get('title', ''),
        'description': job.get('description', ''),
        'url': job.get('externalLink', ''),
        'budget': budget_str,
        'budget_raw': budget,
        'category': job.get('category', ''),
        'experience_level': job.get('vendor', {}).get('experienceLevel', ''),
        'skills': job.get('skills', []),
        'posted': job.get('createdAt', ''),
        'connects_cost': job.get('applicationCost', 0),
        'client': {
            'country': client.get('countryCode', ''),
            'timezone': client.get('timezone', ''),
            'payment_verified': client.get('paymentMethodVerified', False),
            'total_spent': stats.get('totalSpent', 0),
            'total_hires': stats.get('totalHires', 0),
            'hire_rate': stats.get('hireRate', 0),
            'feedback_score': stats.get('feedbackRate', 0),
        },
        'is_featured': job.get('isFeatured', False),
    }


def main():
    parser = argparse.ArgumentParser(description="Scrape Upwork jobs via Apify")

    # Apify filters (free tier)
    parser.add_argument("--limit", "-l", type=int, default=50, help="Max jobs to fetch")
    parser.add_argument("--days", "-d", type=int, help="Only jobs from last N days")
    parser.add_argument("--from-date", help="Jobs posted after (YYYY-MM-DD)")
    parser.add_argument("--to-date", help="Jobs posted before (YYYY-MM-DD)")

    # Actor-level targeting
    parser.add_argument("--keyword", "-k", default="automation,python,n8n,zapier,make.com,openai,api integration,webhook,ai agent,crm automation,hubspot automation,airtable,google sheets automation,lead generation,lead enrichment,cold email automation,apollo,instantly,gmail automation,slack webhook,modal,pdf extraction,lead routing,voice ai", help="Preferred inclusion keywords (comma-separated)")
    parser.add_argument("--exclude-keyword", default="ui/ux,figma,graphic design,video editor,copywriter,virtual assistant,customer support,bookkeeper,seo,social media,newsletter", help="Exclude keywords (comma-separated)")
    parser.add_argument("--categories", help="Preferred job categories (comma-separated)")

    # Post-scrape filters
    parser.add_argument("--max-age-minutes", type=int, default=1440, help="Only jobs posted in last N minutes")
    parser.add_argument("--min-hourly", type=float, help="Minimum hourly rate")
    parser.add_argument("--max-hourly", type=float, help="Maximum hourly rate")
    parser.add_argument("--min-fixed", type=float, default=0, help="Minimum fixed price")
    parser.add_argument("--max-fixed", type=float, help="Maximum fixed price")
    parser.add_argument("--experience", "-e", default="entry,intermediate,expert", help="Experience levels (comma-separated: entry,intermediate,expert)")
    parser.add_argument("--verified-payment", "-v", action="store_true", default=False, help="Only verified payment clients")
    parser.add_argument("--min-spent", type=float, default=0, help="Minimum client total spent ($)")
    parser.add_argument("--min-hires", type=int, default=0, help="Minimum client total hires")

    # Output
    parser.add_argument("--output", "-o", help="Output JSON file")

    args = parser.parse_args()

    # Calculate date range
    from_date = args.from_date
    to_date = args.to_date

    if args.days:
        from_date = (datetime.now() - timedelta(days=args.days)).strftime('%Y-%m-%d')
    elif args.max_age_minutes:
        # If max_age_minutes is small, we still want to fetch from today to be safe
        from_date = datetime.now().strftime('%Y-%m-%d')

    # Scrape jobs
    jobs = scrape_upwork_jobs(
        limit=args.limit,
        from_date=from_date,
        to_date=to_date,
        include_keywords=[k.strip() for k in args.keyword.split(',') if k.strip()],
        exclude_keywords=[k.strip() for k in args.exclude_keyword.split(',') if k.strip()],
        categories=[c.strip() for c in args.categories.split(',') if c.strip()] if args.categories else None,
        payment_verified=True if args.verified_payment else None,
    )

    # Apply post-scrape filters
    experience_levels = args.experience.split(',') if args.experience else None

    filtered_jobs = filter_jobs(
        jobs,
        keyword=args.keyword,
        exclude_keyword=args.exclude_keyword,
        max_age_minutes=args.max_age_minutes,
        min_hourly=args.min_hourly,
        max_hourly=args.max_hourly,
        min_fixed=args.min_fixed,
        max_fixed=args.max_fixed,
        experience_levels=experience_levels,
        verified_payment=args.verified_payment,
        min_client_spent=args.min_spent,
        min_client_hires=args.min_hires,
    )

    # Format jobs
    formatted_jobs = [format_job(job) for job in filtered_jobs]

    # Display results
    print(f"\n=== {len(formatted_jobs)} jobs after filtering ===\n")

    for i, job in enumerate(formatted_jobs[:10], 1):
        print(f"{i}. {job['title'][:70]}")
        print(f"   Budget: {job['budget']} | Level: {job['experience_level']} | Connects: {job['connects_cost']}")
        print(f"   Client: {job['client']['country']} | Spent: ${job['client']['total_spent']:,.0f} | Hires: {job['client']['total_hires']}")
        print(f"   Skills: {', '.join(job['skills'][:5])}")
        print(f"   URL: {job['url']}")
        print()

    if len(formatted_jobs) > 10:
        print(f"... and {len(formatted_jobs) - 10} more jobs")

    # Save to file
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(formatted_jobs, f, indent=2)
        print(f"\nSaved {len(formatted_jobs)} jobs to {args.output}")

    return formatted_jobs


if __name__ == "__main__":
    main()
