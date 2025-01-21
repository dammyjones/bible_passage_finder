import asyncio
from youtube_transcript_api import YouTubeTranscriptApi
import aiofiles
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

# List of Bible books
bible_books = [
    "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy",
    "Joshua", "Judges", "Ruth", "1 Samuel", "2 Samuel", "1 Kings", "2 Kings",
    "1 Chronicles", "2 Chronicles", "Ezra", "Nehemiah", "Esther",
    "Job", "Psalms", "Proverbs", "Ecclesiastes", "Song of Solomon",
    "Isaiah", "Jeremiah", "Lamentations", "Ezekiel", "Daniel",
    "Hosea", "Joel", "Amos", "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk",
    "Zephaniah", "Haggai", "Zechariah", "Malachi",
    "Matthew", "Mark", "Luke", "John", "Acts",
    "Romans", "1 Corinthians", "2 Corinthians", "Galatians",
    "Ephesians", "Philippians", "Colossians",
    "1 Thessalonians", "2 Thessalonians", "1 Timothy", "2 Timothy",
    "Titus", "Philemon", "Hebrews", "James", "1 Peter", "2 Peter",
    "1 John", "2 John", "3 John", "Jude", "Revelation"
]

# Extract video ID from URL
def get_video_id(url):
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]
    return url.split("/")[-1]

def split_transcript_into_chunks(transcript, chunk_size):
    words = transcript.split()
    return [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

# Find text in JSON (KJV.json)
async def find_bible_passage(book, chapter, verse, bible_data):
    """Find a Bible passage and return it with book, chapter, and verse."""
    for book_data in bible_data["books"]:
        if book_data["name"] == book:
            for ch in book_data["chapters"]:
                if ch["chapter"] == chapter:
                    for v in ch["verses"]:
                        if v["verse"] == verse:
                            return f"{book} {chapter}:{verse} - {v['text']}\n"
                    # If verse is not found, return the first verse
                    return f"{book} {chapter}:1 - {ch['verses'][0]['text']}\n"
    return "Passage not found."

# Find text in JSON
async def find_text_in_json(chunk, bible_data):
    for book_data in bible_data["books"]:
        for ch in book_data["chapters"]:
            for v in ch["verses"]:
                if chunk in v["text"]:
                    return book_data["name"], ch["chapter"], v["verse"], v["text"]
    return None

async def main():
    video_url = "https://www.youtube.com/watch?v=_JBKVEV7NQs&pp=ygUNcGFzdG9yIGt1bXV5aQ%3D%3D"
    video_id = get_video_id(video_url)
    
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
    except Exception as e:
        logging.error(f"Failed to retrieve transcript: {e}")
        return
    
    full_transcript = " ".join(entry["text"] for entry in transcript)
    
    # Replace terms and clean up transcript
    replacements = {'verse': ':', 'chapter': ' ' }
    for word, replacement in replacements.items():
        full_transcript = full_transcript.replace(word, replacement)

    words = full_transcript.split()

    # Load the Bible JSON data
    try:
        async with aiofiles.open("KJV.json", mode='r') as f:
            bible_data = json.loads(await f.read())
    except Exception as e:
        logging.error(f"Failed to load Bible data: {e}")
        return

    # Search for Bible books, chapters, and verses
    for i in range(len(words) - 2):  # Adjusted loop to avoid out-of-range
        if words[i] in bible_books:
            try:
                chapter = int(words[i + 1]) # Validate chapter as an integer
                verse = str(words[i + 2]).replace(".", "")  # Keep verse as string to handle ranges
                logging.info(f"Book: {words[i]}, Chapter: {chapter}, Verse: {verse}")
                verses = []
                if '-' in str(verse):
                    try:
                        start_verse, end_verse = map(int, verse.split("-"))
                        for v in range(start_verse, end_verse + 1):
                            passage = await find_bible_passage(words[i], chapter, v, bible_data)
                            verses.append(passage)
                    except ValueError:
                        logging.error(f"Invalid verse range: {verse}")
                        continue
                else:
                    try:
                        passage = await find_bible_passage(words[i], chapter, int(verse), bible_data)
                    except ValueError:
                        passage = await find_bible_passage(words[i], chapter, 1, bible_data)
                    verses.append(passage)

                async with aiofiles.open("passage.txt", "a") as file:
                    await file.write("".join(verses) + "\n")
                logging.info("".join(verses))

            except ValueError:
                # Skip if chapter or verse is not a valid integer or format
                continue
    
    # Split transcript into chunks
    chunk_size = 4  # Adjust chunk size
    chunks = split_transcript_into_chunks(full_transcript, chunk_size)

    # Search each chunk in the JSON
    for chunk in chunks:
        result = await find_text_in_json(chunk, bible_data)
        if result:
            book, chapter, verse, text = result
            logging.info(f"Found in Bible: {book} {chapter}:{verse} - {text}")
            async with aiofiles.open("passage2.txt", "a") as file:
                await file.write(f"{book} {chapter}:{verse} - {text}\n")

# Run the async main function
asyncio.run(main())
