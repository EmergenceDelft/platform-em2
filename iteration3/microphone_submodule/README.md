# Iteration 3 Speech Recognition and Synthesis

`speech_to_text.py` listens to microphone input and translates it to text. `text_to_speech.py` reads out the text to digital output.

## Setup

This section details setup instructions for speech recognition and text to speech scripts.

### Adjusting sound devices

When you run the programme you'll be able to see a list of audio devices available on your machine. In order to make the code compatible with Ableton, for input device choose your microphone and for output it will be: Dante Via/Jack (on Windows) or Blackhole (on mac).

#### Changing it in files
In `speech_to_text.py` you might have to change **line 20**:
```angular2html
recording = sd.rec(int(duration * fs), samplerate=fs, device = 1, dtype = 'int16', mapping=[2])
```

In `text_to_speech.py` you might have to change **line 50**:
```angular2html
sd.play(data, samplerate, device = 6, mapping=[40])
```

In both cases you can change both the device (microphone, Backhole, etc.) and mapping (the channel you want to play/record to).

#### Example list of devices:
```
sounddevice audio devices:
   0 Microsoft Sound Mapper - Input, MME (2 in, 0 out)
   1 Dante Via Receive (Dante Via), MME (2 in, 0 out)
   2 Headset (Jabra Headphones ), MME (2 in, 0 out)
   3 Microfoonmatrix (Intel® Smart S, MME (2 in, 0 out)
   4 Microsoft Sound Mapper - Output, MME (0 in, 2 out)
   5 Headphones (Jabra Headphones ), MME (0 in, 2 out)
   6 Speakers (Realtek(R) Audio), MME (0 in, 2 out)
   7 Dante Via Transmit (Dante Via), MME (0 in, 2 out)
speechrecognition microphones:
    0, Microsoft Sound Mapper - Input
    1, Dante Via Receive (Dante Via)
    2, Headset (Jabra Headphones )
    3, Microfoonmatrix (IntelÂ® Smart S
    4, Microsoft Sound Mapper - Output
    5, Headphones (Jabra Headphones )
    6, Speakers (Realtek(R) Audio)
    7, Dante Via Transmit (Dante Via)

```

### Parameters

In `text_to_speech.py`:
* `input_file_path = "audio_files/at_home_testing.txt"` - the location of text that was transcribed in the space
* `audio_file_path = 'audio_files/mac_computer.aiff'` - the file with read text
* `WAIT = 5` - in this case after 5 second the text from `input_file_path` will be read again

In `speech_to_text.py`:
* `DURATION = 12`  - Duration of speech recording in seconds
* `TRANSCRIPTIONS = 2` - Number of transcriptions that are saved
* `output_file = "audio_files/recorded_audio_1.wav"` - location of recorded audio that should be transcribed
* `text_file_path = "audio_files/at_home_testing.txt"` - location of text that was transcribed

## Run instructions

1. Make sure you are in the virtual environment/have all dependencies installed.
2. Install ffmpeg using `brew install ffmpeg`
3. If needed you can adjust parameters from [Parameters section](#parameters)
4. Run both `speech_to_text.py` and `text_to_speech.py`

## Troubleshooting 
Something doesn't work? Try this:

1. Are your devices properly setup? - look into [sound devices section](#adjusting-sound-devices)
2. Is your mapping properly setup? - look into [sound devices section](#adjusting-sound-devices)
3. Do you correct number of channels for the device you're using? - you might have to change lines showed in [this section](#changing-it-in-files)
4. Are you not using conflicting channels? - The composition might use up to 35 channels from Blackhole, make sure you are using a different device or higher number.
5. Are you using Windows and `text_to_speech.py` is not working? - you might have to adjust some things in the script, it was made to work on Mac.