import speech_recognition as sr
import sounddevice as sd
import soundfile as sf
import pyttsx3

def recognize_speech(m, r):

    with m as source:
        print("Say something!")
        audio = r.listen(source, phrase_time_limit=5)
    try:
        print("Speech recognized!")
        text = r.recognize_google(audio)
        print("I heared: " + text)
        return text
    except sr.UnknownValueError:
        print("Could not understand the text.")
        return "say again"

def say_text(speaker, recognized_text):
    print("I'm saying: " + recognized_text)
    speaker.save_to_file(recognized_text, 'windows_computer.wav')
    speaker.runAndWait()
    try:
        data, samplerate = sf.read('windows_computer.wav')
        sd.play(data, samplerate, device=1, mapping=[30])
        sd.wait()
    except Exception as e:
        print(e)


def list_devices():
    print("sounddevice audio devices:")
    print(sd.query_devices())

    print("speechrecognition microphones:")
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print(f'{index}, {name}')


def main_loop(speaker, r, m):
    while True:
        text = recognize_speech(m, r)
        say_text(speaker, text)


if __name__ == "__main__":
    # obtain audio from the microphone
    r = sr.Recognizer()
    m = sr.Microphone(device_index=0)
    with m as source:
        r.adjust_for_ambient_noise(source)

    speaker = pyttsx3.init()

    list_devices()
    main_loop(speaker, r, m)
