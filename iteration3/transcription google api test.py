import time
from google.cloud import texttospeech
from pydub import AudioSegment
from pydub.playback import play
import sounddevice as sd
import soundfile as sf



def synthesize_text(text):
    """Synthesizes speech from the input string of text."""
    # Initialize the Text-to-Speech client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    input_text = texttospeech.SynthesisInput(text=text)

    # Specify the voice parameters
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-casual-K",
        ssml_gender=texttospeech.SsmlVoiceGender.MALE,
    )

    # Specify the audio configuration
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request
    response = client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )

    # Write the response's audio content to an output file
    output_file_path = r"C:\Users\simon\Documents\1Simon\emergence\platform\experiment\live transcription\test1.mp3"
    with open(output_file_path, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{output_file_path}"')

    return output_file_path

def read_text_from_file(file_path):
    """Reads text from a .txt file."""
    with open(file_path, 'r', encoding='ISO-8859-1') as file:
        return file.read()

def play_audio(file_path):
    """Plays the audio file."""
    audio = AudioSegment.from_mp3(file_path)
    play(audio)

# Path to the input .txt file
input_file_path = r"C:\Users\simon\Documents\1Simon\emergence\platform\experiment\live transcription\at_home_testing.txt"
while True:
    # Read text from the file
    input_text = read_text_from_file(input_file_path)
    
    # Synthesize text to speech and get the path of the output audio file
    audio_file_path = synthesize_text(input_text)
    
    #Play the generated audio file
    play_audio(audio_file_path)
    
    # Wait for 10 seconds before repeating
    time.sleep(20)
