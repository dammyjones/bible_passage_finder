import pyaudio
import whisper
import numpy as np

# Initialize Whisper model
model = whisper.load_model("base")  # You can choose 'small', 'medium', 'large' for different accuracy/performance tradeoffs

def transcribe_audio_stream(stream, chunk_size, rate):
    print("Starting transcription...")
    
    while True:
        try:
            # Read audio from the microphone stream
            audio_data = stream.read(chunk_size)
            
            # Convert audio to a format Whisper can process
            audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32)
            audio_np = audio_np / 32768.0  # Normalize to [-1, 1] range
            
            # Convert the numpy array to a suitable format for Whisper
            audio = np.array(audio_np)

            # Perform transcription
            result = model.transcribe(audio)
            
            # Print the transcription result
            print("Transcript:", result['text'])
        except Exception as e:
            print(f"Error during transcription: {e}")

def start_recording_and_transcribing():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000

    # Initialize PyAudio
    audio = pyaudio.PyAudio()

    # Open the microphone stream
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                        input=True, frames_per_buffer=CHUNK)

    try:
        print("Recording and transcribing...")
        transcribe_audio_stream(stream, CHUNK, RATE)
    except KeyboardInterrupt:
        print("\nStopping recording and transcription...")
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()
        print("Resources cleaned up.")

if __name__ == "__main__":
    start_recording_and_transcribing()
