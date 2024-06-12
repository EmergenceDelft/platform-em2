import os
import sounddevice as sd
import numpy as np
from pydub import AudioSegment
import whisper
import time

print ("hello world")
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
    
duration = 15  # Duration to record in seconds
