import json
import os

def verify():
    if not os.path.exists('tmp/upwork/merged_leads.json'):
        print("merged_leads.json not found")
        return
        
    with open('tmp/upwork/merged_leads.json', 'r') as f:
        jobs = json.load(f)
        
    print(f"Total leads: {len(jobs)}")
    for i, job in enumerate(jobs[:10], 1):
        desc = job.get('description', '')
        print(f"{i}. {len(desc)} chars: {job.get('title')[:60]}")
        if len(desc) > 0:
            print(f"   START: {desc[:100]}...")
            print(f"   END:   ...{desc[-100:]}")
            print("-" * 20)

if __name__ == "__main__":
    verify()
