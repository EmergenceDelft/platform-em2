from midi_sender import MidiSender
import time

midi_sender = MidiSender('platform midi Port 1')

while True:
  act = 1
  print(f"Activating cc {act} with value 50")

  midi_sender.send_control_change(channel = 0, control = act, value = 50)
  time.sleep(0.15)