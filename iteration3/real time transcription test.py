import os
import sounddevice as sd
import numpy as np
from pydub import AudioSegment
import whisper
import time

def record_audio(duration, output_file):
    
    # Record audio from the microphone
    try:
        fs = 48000  # Sample rate
        print(f"Recording {duration} seconds of audio...")
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=2, dtype='int16')
        sd.wait()  # Wait until recording is finished
        print("Recording finished")
        
        # Verify if recording was successful
        if recording is None or len(recording) == 0:
            print("Recording failed or no data captured")
            return False

        audio_array = np.array(recording)
        audio_segment = AudioSegment(
            audio_array.tobytes(),
            frame_rate=fs,
            sample_width=audio_array.dtype.itemsize,
            channels=2
        )
        audio_segment.export(output_file, format="wav")
        print(f"Audio recorded and saved to {output_file}")
        return True
    except Exception as e:
        print(f"Error while recording audio: {e}")
        return False

def transcribe_audio(file_path):
    try:
        if not os.path.exists(file_path):
            print(f"Audio file {file_path} does not exist")
            return ""
        
        # Load the Whisper model
        print("Loading Whisper model...")
        model = whisper.load_model("base")

        # Transcribe the audio file
        print(f"Transcribing audio file {file_path}...")
        result = model.transcribe(file_path)
        
        # Return the transcribed text
        transcription = result['text']
        print(f"Transcription: {transcription}")
        return transcription
    except Exception as e:
        print(f"Error while transcribing audio: {e}")
        return ""

def save_transcription_to_text(transcription, text_file_path):
    try:
        if transcription:
            with open(text_file_path, 'a') as f:
                f.write(transcription + "\n")
            print(f"Transcription saved to {text_file_path}")
        else:
            print("No transcription to save")
    except Exception as e:
        print(f"Error while saving transcription to text file: {e}")

# Parameters
duration = 15  # Duration to record in seconds
output_file = r"C:\Users\simon\Documents\1Simon\emergence\platform\experiment\live transcription\recorded_audio_resonator_test.wav"
text_file_path = r"C:\Users\simon\Documents\1Simon\emergence\platform\experiment\live transcription\resonator_transcription.txt"

print(f"Output audio file will be saved to: {output_file}")
print(f"Transcriptions will be saved to: {text_file_path}")


while True:
    # Record audio
    if record_audio(duration, output_file):
        # Transcribe the recorded audio
        transcription = transcribe_audio(output_file)

        # Save the transcription to a text file
        save_transcription_to_text(transcription, text_file_path)
    else:
        print("Recording was not successful. Skipping transcription and saving.")

        # Wait for a few seconds before recording the next segment
        time.sleep(2)
