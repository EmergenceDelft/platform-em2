# Iteration 2 Speech Recognition and Synthesis

The script listens to microphone input, translates it to text and reads out the text to computer output.

## Setup

### Virtual Environment
Create a virtual environment and activate it, a user guide can be found [here](https://docs.python.org/3/library/venv.html).

Example for mac:
```
python3 -m venv env
source env/bin/activate
```

**Install requirements:**
```
pip3 install -r requirements.txt
```

### Running the code
On mac run the code using:
```
python3 mac_sync_speech.py
```

On windows:
```
python3 windows_sync_speech.py
```

## Adjusting sound devices

When you run the programme you'll be able to see a list of audio devices available on your machine. In order to make the code compatible with Ableton, for input device choose your microphone and for output Either Dante Via (on windows) or Blackhole (on mac).

Exmple list of devices:
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

