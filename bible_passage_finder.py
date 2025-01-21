from youtube_transcript_api import YouTubeTranscriptApi
import csv
import asyncio

# List of Bible books
bible_books = [
    # Old Testament
    "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy",  
    "Joshua", "Judges", "Ruth",  
    "1 Samuel", "2 Samuel", "1 Kings", "2 Kings", 
    "1 Chronicles", "2 Chronicles", "Ezra", "Nehemiah", "Esther",
    "Job", "Psalms", "Proverbs", "Ecclesiastes", "Song of Solomon",  
    "Isaiah", "Jeremiah", "Lamentations", "Ezekiel", "Daniel",  
    "Hosea", "Joel", "Amos", "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk",
    "Zephaniah", "Haggai", "Zechariah", "Malachi",  

    # New Testament
    "Matthew", "Mark", "Luke", "John",  
    "Acts",  
    "Romans", "1 Corinthians", "2 Corinthians", "Galatians", 
    "Ephesians", "Philippians", "Colossians", 
    "1 Thessalonians", "2 Thessalonians", "1 Timothy", "2 Timothy", 
    "Titus", "Philemon",  
    "Hebrews", "James", "1 Peter", "2 Peter", "1 John", "2 John", "3 John", "Jude",  
    "Revelation"
]

# Extract video ID from URL
def get_video_id(url):
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]
    return url.split("/")[-1]

# URL of the video
video_url = "https://www.youtube.com/watch?v=iOXJ9uWhigA&pp=ygUldGhlc2UgMTUgdmVyc2VzIHdpbGwgY2hhbmdlIHlvdXIgbGlmZQ%3D%3D"
video_id = get_video_id(video_url)

import csv

# Function to search for a specific book, chapter, and verse in a CSV
def find_bible_passage(book, chapter, verse):
    file_path = "KJV.csv"
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Check for the match of Book, Chapter, and Verse
            if row['Book'] == book and int(row['Chapter']) == chapter and int(row['Verse']) == verse:
                return f"{row['Text']}\n"
    return "Passage not found."
def split_transcript_into_chunks(transcript, chunk_size):
    words = transcript.split()
    return [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]


            
try:
    # Fetch the transcript (list of dictionaries)
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    
    # Combine all the text into a single string
    full_transcript = " ".join(entry["text"] for entry in transcript)
    
    # Define replacements
    replacements = {
        'verse': ':',
        'chapter': ' '
    }
    
    # Apply replacements
    for word, replacement in replacements.items():
        full_transcript = full_transcript.replace(word, replacement)
    
    # Split the transcript into words
    words = full_transcript.split()
    counter=0
    # Search for Bible books, chapters, and verses
    for i in range(len(words) - 3):  # Avoid index out-of-range
        if words[i] in bible_books:
            try:
                
                chapter = int(words[i + 1])  # Validate chapter as an integer
                verse = int(words[i + 3])  # Validate verse as an integer
                print(f"Book: {words[i]}, Chapter: {chapter}, Verse: {verse}")
                counter+=1
                with open("passage.txt", "a") as file:
                    file.write(find_bible_passage(words[i], chapter, verse))
                print(find_bible_passage(words[i], chapter, verse))
               
            except ValueError:
                # Skip if chapter or verse is not a valid integer
                continue
    print(counter)
except Exception as e:
    print(f"Error: {e}")
def split_transcript_into_chunks(transcript, chunk_size):
    words = transcript.split()
    return [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

# Find text in CSV
def find_text_in_csv(chunk, file_path="KJV.csv"):
    try:
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if chunk in row['Text']:
                    return row['Book'], row['Chapter'], row['Verse'], row['Text']
    except Exception as e:
        print(f"Error reading CSV: {e}")
    return None

# Main script execution
try:
    video_url = "https://www.youtube.com/watch?v=iOXJ9uWhigA&pp=ygUldGhlc2UgMTUgdmVyc2VzIHdpbGwgY2hhbmdlIHlvdXIgbGlmZQ%3D%3D"
    video_id = get_video_id(video_url)
    
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    full_transcript = " ".join(entry["text"] for entry in transcript)
    
    # Replace terms and clean up transcript
    replacements = {'verse': ':', 'chapter': ' '}
    for word, replacement in replacements.items():
        full_transcript = full_transcript.replace(word, replacement)
    
    # Split transcript into chunks
    chunk_size = 4  # Adjust chunk size
    chunks = split_transcript_into_chunks(full_transcript, chunk_size)
    
    # Search each chunk in the CSV
    for chunk in chunks:
        result = find_text_in_csv(chunk)
        if result:
            book, chapter, verse, text = result
            print(f"Found in Bible: {book} {chapter}:{verse} - {text}")
            with open("passage2.txt", "a") as file:
                file.write(f"{book} {chapter}:{verse} - {text}\n")
        else:
            pass

except Exception as e:
    print(f"Error: {e}")
