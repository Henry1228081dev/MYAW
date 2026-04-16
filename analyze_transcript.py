import sys

def parse_transcript(file_path):
    keywords = ["directive", "orchestration", "execution", "doe", "supabase", "modal", "langgraph", "crewai", "agency", "pricing"]
    results = {k: [] for k in keywords}
    
    try:
        with open(file_path, 'r', encoding='utf-16') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                line_lower = line.lower()
                for k in keywords:
                    if k in line_lower:
                        # Grab a window of context
                        start = max(0, i - 2)
                        end = min(len(lines), i + 3)
                        context = " ".join([l.strip() for l in lines[start:end]])
                        results[k].append(context)
                        break # avoid double counting in same line if multiple keywords
                        
        # Write summary
        with open("saraev_analysis.txt", "w", encoding='utf-8') as out:
            for k, excerpts in results.items():
                out.write(f"--- KEYWORD: {k.upper()} ({len(excerpts)} mentions) ---\n")
                # Just write first 10 occurrences to get the gist
                for ex in excerpts[:10]:
                    out.write(f"- {ex}\n")
                out.write("\n")
        print("Analysis complete. Saved to saraev_analysis.txt")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    parse_transcript("MxyRjL7NG18_transcript.txt")
