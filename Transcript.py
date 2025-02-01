import speech_recognition as sr
import threading
import time

# Initialize recognizer
recognizer = sr.Recognizer()

# Keyword to stop the program
EXIT_KEYWORD = "exit"

# File to save transcriptions
TRANSCRIPTION_FILE = "transcription.txt"

def transcribe_audio(audio):
    """Convert speech to text and log the result."""
    try:
        text = recognizer.recognize_google(audio)
        print(f"\nYou said: {text}")
        
        # Save transcription to file
        with open(TRANSCRIPTION_FILE, "a") as file:
            file.write(text + "\n")
        
        # Stop if exit keyword is detected
        if EXIT_KEYWORD in text.lower():
            print("\nExit keyword detected. Stopping transcription...")
            return False

    except sr.UnknownValueError:
        print("\n[Error] Could not understand audio")
    except sr.RequestError as e:
        print(f"\n[Error] API request failed: {e}")

    return True

def listen_continuously():
    """Continuously listens for speech and processes it in a separate thread."""
    with sr.Microphone() as source:
        print("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source, duration=2)
        print("\nListening for speech... (Say 'exit' to stop)")

        while True:
            try:
                # Listen for speech
                audio = recognizer.listen(source)

                # Start a thread to process the audio asynchronously
                thread = threading.Thread(target=transcribe_audio, args=(audio,))
                thread.start()

                # Small delay to prevent excessive CPU usage
                time.sleep(0.5)

            except KeyboardInterrupt:
                print("\n[INFO] Stopped by user.")
                break

if __name__ == "__main__":
    listen_continuously()
