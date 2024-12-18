import os
import sounddevice as sd
import numpy as np
from pydub import AudioSegment
import speech_recognition as sr
import time

# Parameters
DURATION = 12  # Duration to record in seconds
TRANSCRIPTIONS = 4


output_file = "recorded_audio_1.wav"
text_file_path = "at_home_testing.txt"
def record_audio(duration, output_file):
    # Record audio from the microphone
    try:
        fs = 48000  # Sample rate
        print(f"Recording {duration} seconds of audio...")
        #recording = sd.rec(int(duration * fs), samplerate=fs, device = 1, dtype = 'int16', mapping=[2])
        recording = sd.rec(int(duration * fs), samplerate=fs, device = 1, dtype = 'int16', mapping=[2])
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
            channels = 1
        )
        audio = audio_segment.export(output_file, format="wav")
        print(f"Audio recorded and saved to {output_file}")
        return audio
    except Exception as e:
        print(f"Error while recording audio: {e}")
        return False

def transcribe_audio(model, file_path):
    try:
        if not os.path.exists(file_path):
            print(f"Audio file {file_path} does not exist")
            return ""
        with sr.AudioFile(file_path) as source:
            audio = model.record(source)  # read the entire audio file

        # Transcribe the audio file
        print(f"Transcribing audio file ...")
        result = None
        try:
            result = model.recognize_google(audio)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        #result = model.transcribe(file_path, fp16=False)
        
        # Return the transcribed text
        transcription = result
        print(f"Transcription: {transcription}")
        return transcription
    except Exception as e:
        print(f"Error while transcribing audio: {e}")
        return ""

def save_transcription_to_text(transcription, text_file_path):
    try:
        # Read existing transcriptions
        if os.path.exists(text_file_path):
            with open(text_file_path, 'r') as f:
                existing_transcriptions = f.readlines()
        else:
            existing_transcriptions = []
        
        # Append new transcription
        if transcription != None:
            existing_transcriptions.append(transcription + "\n")
        
        # Keep only the last 3 transcriptions
        if len(existing_transcriptions) > TRANSCRIPTIONS:
            existing_transcriptions = existing_transcriptions[-TRANSCRIPTIONS:]
        
        # Write back to file
        with open(text_file_path, 'w') as f:
            f.writelines(existing_transcriptions)
        
        print(f"Transcription saved to {text_file_path}")
    except Exception as e:
        print(f"Error while saving transcription to text file: {e}")


def main():
    print(sd.query_devices())
    print(f"Output audio file will be saved to: {output_file}")
    print(f"Transcriptions will be saved to: {text_file_path}")
    # Load the Whisper model
    #print("Loading Whisper model...")
    #model = whisper.load_model("base")
    model = sr.Recognizer()

    try:
        while True:
            # Record audio
            if record_audio(DURATION, output_file):
                # Transcribe the recorded audio
                transcription = transcribe_audio(model, output_file)

                # Save the transcription to a text file
                save_transcription_to_text(transcription, text_file_path)
            else:
                print("Recording was not successful. Skipping transcription and saving.")

            # Wait for a few seconds before recording the next segment
            time.sleep(1)
    except KeyboardInterrupt:
        print("Recording stopped by user.")


if __name__ == "__main__":
    main()