from youtube_transcript_api import YouTubeTranscriptApi
import pandas as pd

# Function to get the video ID from a URL
def get_video_id(url):
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]
    return url.split("/")[-1]

# Fetch transcript
video_url = "https://www.youtube.com/watch?v=0bbG3RasIfM&pp=ygURcGFzdG9yIGVhIGFkZWJveWU%3D"
video_id = get_video_id(video_url)
transcript = YouTubeTranscriptApi.get_transcript(video_id)

# Group transcript by 30-second intervals
def group_transcript_by_time(transcript, interval=30):
    grouped_transcript = []
    current_group = []
    current_start_time = 0

    for entry in transcript:
        start_time = entry["start"]
        text = entry["text"]

        # If the entry falls within the current interval, add it to the group
        if start_time < current_start_time + interval:
            current_group.append(text)
        else:
            # Save the current group as a single row and start a new group
            grouped_transcript.append({
                "Start Time (s)": current_start_time,
                "End Time (s)": current_start_time + interval,
                "Transcript": " ".join(current_group)
            })
            current_start_time += interval
            current_group = [text]

    # Add the final group
    if current_group:
        grouped_transcript.append({
            "Start Time (s)": current_start_time,
            "End Time (s)": current_start_time + interval,
            "Transcript": " ".join(current_group)
        })

    return grouped_transcript

# Group transcript into 30-second intervals
grouped_transcript = group_transcript_by_time(transcript, interval=30)

# Convert to DataFrame
df = pd.DataFrame(grouped_transcript)

# Save to Excel
df.to_csv("Bible passage data.csv", index=False)
print("Transcript split into 30-second intervals and saved to 'transcript_30s_intervals.csv'")
