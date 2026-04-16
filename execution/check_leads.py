import json
import os

def count_leads():
    raw_jobs = []
    fresh_jobs = []
    
    if os.path.exists('tmp/upwork/raw_jobs.json'):
        with open('tmp/upwork/raw_jobs.json', 'r') as f:
            raw_jobs = json.load(f)
            
    if os.path.exists('.tmp/fresh_upwork_jobs.json'):
        with open('.tmp/fresh_upwork_jobs.json', 'r') as f:
            fresh_jobs = json.load(f)
            
    all_jobs = raw_jobs + fresh_jobs
    unique_ids = set()
    unique_jobs = []
    
    for job in all_jobs:
        jid = job.get('id') or job.get('uid')
        if jid and jid not in unique_ids:
            unique_ids.add(jid)
            unique_jobs.append(job)
            
    print(f"Raw jobs: {len(raw_jobs)}")
    print(f"Fresh jobs: {len(fresh_jobs)}")
    print(f"Total unique jobs: {len(unique_jobs)}")
    return unique_jobs

if __name__ == "__main__":
    count_leads()
