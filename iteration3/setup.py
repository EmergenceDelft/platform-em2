from midi_sender import MidiSender
import time

midi_sender = MidiSender('platform midi Port 1')

# change to activate different cc
activate_cc = 0

while True:

  print(f"Activating cc {activate_cc} with value 50")

  midi_sender.send_control_change(channel = 0, control = activate_cc, value = 50)
  time.sleep(0.15)