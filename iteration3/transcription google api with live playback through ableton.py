import time
from google.cloud import texttospeech
from pydub import AudioSegment
from pydub.playback import play
import sounddevice as sd
import soundfile as sf
import librosa

print("Querying audio devices...")
print(sd.query_devices())
print("Checking output settings for device 1...")
print(sd.check_output_settings(device=18))

def synthesize_text(text):
    """Synthesizes speech from the input string of text."""
    print("Initializing Text-to-Speech client...")
    client = texttospeech.TextToSpeechClient()

    print("Setting text input to be synthesized...")
    input_text = texttospeech.SynthesisInput(text=text)
    

    print("Specifying voice parameters...")
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-casual-K",
        ssml_gender=texttospeech.SsmlVoiceGender.MALE,
    )

    print("Specifying audio configuration...")
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    print("Performing text-to-speech request...")
    print(input_text)
    response = client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )
    

    output_file_path = r"C:\Users\simon\Documents\1Simon\emergence\platform\experiment\live transcription\test1.mp3"
    print(f"Writing audio content to file \"{output_file_path}\"...")
    with open(output_file_path, "wb") as out:
        out.write(response.audio_content)

    print(f"Audio content written to file \"{output_file_path}\"")
    return output_file_path

def read_text_from_file(file_path):
    """Reads text from a .txt file."""
    print(f"Reading text from file \"{file_path}\"...")
    with open(file_path, 'r', encoding='ISO-8859-1') as file:
        return file.read()

def resample_audio(audio_file_path, target_sample_rate=48000):
    """Resamples audio to the target sample rate."""
    print(f"Reading audio file \"{audio_file_path}\" for resampling...")
    data, samplerate = sf.read(audio_file_path)
    print(f"Original sample rate: {samplerate}, Target sample rate: {target_sample_rate}")

    if samplerate != target_sample_rate:
        print("Resampling audio...")
        data_resampled = librosa.resample(data.T, orig_sr=samplerate, target_sr=target_sample_rate)
        data_resampled = data_resampled.T
        resampled_file_path = audio_file_path.replace(".mp3", "_resampled.wav")
        sf.write(resampled_file_path, data_resampled, target_sample_rate)
        print(f"Resampled audio written to \"{resampled_file_path}\"")
        return resampled_file_path
    else:
        print("Sample rate matches target. No resampling needed.")
        return audio_file_path

def play_audio(audio_file_path):
    try:
        print(f"Preparing to play audio file \"{audio_file_path}\"...")
        resampled_audio_file_path = resample_audio(audio_file_path)
        
        print(f"Playing audio file \"{resampled_audio_file_path}\"...")
        data, samplerate = sf.read(resampled_audio_file_path)
        sd.play(data, samplerate, device=20, mapping=[10])
        sd.wait()
        print("Audio playback completed.")
    except Exception as e:
        print(f"Error during audio playback: {e}")

# Path to the input .txt file
input_file_path = r"C:\Users\simon\Documents\1Simon\emergence\platform\experiment\live transcription\at_home_testing.txt"

while True:
    # Read text from the file
    input_text = read_text_from_file(input_file_path)
    
    # Synthesize text to speech and get the path of the output audio file
    audio_file_path = synthesize_text(input_text)
    
    # Play the generated audio file
    play_audio(audio_file_path)
    
    # Wait for 22 seconds before repeating
    print("Waiting for 22 seconds before repeating...")
    time.sleep(22)
