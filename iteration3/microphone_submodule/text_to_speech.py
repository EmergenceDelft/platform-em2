import librosa
import soundfile as sf
import sounddevice as sd
from macos_speech import Synthesizer
import time
#import pyttsx3

mac = True
# Path to the input .txt file
input_file_path = "iteration3/microphone_submodule/audio_files/at_home_testing.txt"
audio_file_path = 'iteration3/microphone_submodule/audio_files/mac_computer.aiff'
WAIT = 5


def read_text_from_file (file_path):
  """Reads text from a .txt file."""
  print(f"Reading text from file \"{file_path}\"...")
  with open(file_path, 'r', encoding='ISO-8859-1') as file:
      return file.read()


def resample_audio (audio_file_path, target_sample_rate=48000):
  """Resamples audio to the target sample rate."""
  print(f"Reading audio file \"{audio_file_path}\" for resampling...")
  data, samplerate = sf.read(audio_file_path)
  print(f"Original sample rate: {samplerate}, Target sample rate: {target_sample_rate}")

  if samplerate != target_sample_rate:
    print("Resampling audio...")
    data_resampled = librosa.resample(data.T, orig_sr = samplerate, target_sr = target_sample_rate)
    data_resampled = data_resampled.T
    resampled_file_path = audio_file_path.replace(".mp3", "_resampled.wav")
    sf.write(resampled_file_path, data_resampled, target_sample_rate)
    print(f"Resampled audio written to \"{resampled_file_path}\"")
    return resampled_file_path
  else:
    print("Sample rate matches target. No resampling needed.")
    return audio_file_path

def mac_say_text(speaker, text):

  speaker.say(text)


def mac_say_text (speaker, recognized_text, file_name):
  print("I'm saying: " + recognized_text)
  speaker.say(recognized_text)
  try:
    data, samplerate = sf.read(file_name)
    sd.play(data, samplerate, device = 6, mapping=[40])
    sd.wait()
  except Exception as e:
    print(e)

def main():
  print(sd.query_devices())

  
  speaker = Synthesizer(outfile=audio_file_path)
  

  while True:
    # Read text from the file
    input_text = read_text_from_file(input_file_path)

    
    mac_say_text(speaker, input_text, audio_file_path)
    

    # Wait for 22 seconds before repeating
    print(f"Waiting for {WAIT} seconds before repeating...")
    time.sleep(WAIT)

if __name__ == "__main__":
  main()