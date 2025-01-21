import pyaudio
import wave

def save_audio_to_wav(filename, audio_format, channels, rate, chunk_size, stream):
    print(f"Recording audio to {filename}...")
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(audio_format.get_sample_size(FORMAT))
        wf.setframerate(rate)

        try:
            while True:
                data = stream.read(chunk_size, exception_on_overflow=False)
                wf.writeframes(data)  # Write audio frames to file
        except KeyboardInterrupt:
            print("\nStopping recording...")

if __name__ == "__main__":
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000

    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    try:
        save_audio_to_wav("output.wav", audio, CHANNELS, RATE, CHUNK, stream)
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()
        print("Recording saved and resources cleaned up.")

