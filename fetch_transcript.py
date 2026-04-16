import sys
from youtube_transcript_api import YouTubeTranscriptApi

def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        with open(f"{video_id}_transcript.txt", "w", encoding="utf-8") as f:
            for entry in transcript:
                f.write(f"{entry['text']}\n")
        print(f"Successfully saved transcript to {video_id}_transcript.txt")
    except Exception as e:
        print(f"Error fetching transcript: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python fetch_transcript.py <video_id>")
    else:
        get_transcript(sys.argv[1])
