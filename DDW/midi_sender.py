import mido
import numpy as np

class MidiSender:
  def __init__ (self, port_name=None, num_reg=4, smooth = 0.5):
    """
    Initialize the MidiSender class.

    :param port_name: Name of the MIDI port to open. If None, the default output port will be used.
    """
    self.port_name = port_name
    self.output = None
    if port_name not in mido.get_output_names():
        print(f"Error: MIDI port '{port_name}' not found.")
        return
    self.open_port()
    self.min_midi = 0
    self.max_midi = 127

    self.smooth = smooth
    self.movement = 0
    self.circle = 0
    self.grid = np.zeros(num_reg)
    self.detections = 0

  def open_port (self):
    """
    Open the MIDI port for sending messages.
    """
    if self.port_name:
      self.output = mido.open_output(self.port_name)
    else:
      self.output = mido.open_output()

  def reset(self):
    self.min_midi = 0
    self.max_midi = 127
  def close_port (self):
    """
    Close the MIDI port.
    """
    if self.output:
      self.output.close()
      self.output = None

  def send_control_change (self, channel, control, value):
    """
    Send a Control Change message.

    :param channel: MIDI channel (0-15)
    :param control: Control number (0-127)
    :param value: Control value (0-127)
    """
    msg = mido.Message('control_change', channel = channel, control = control, value = value)
    self.output.send(msg)

  def send_mean_movement (self, channel, control, movement):
    """
    Send a Control Change message.

    :param channel: MIDI channel (0-15)
    :param control: Control number (0-127)
    :param value: Control value (0-127)
    """
    new_movement = int(self.movement * (1 - self.smooth) + movement * self.smooth)
    self.movement = new_movement
    msg = mido.Message('control_change', channel = channel, control = control, value = new_movement)
    self.output.send(msg)

  def send_circle_score(self, channel, control, circle):
    """
    Send a Control Change message.

    :param channel: MIDI channel (0-15)
    :param control: Control number (0-127)
    :param circle: Control value (0-127)
    """
    new_circle = int(self.circle * (1 - self.smooth) + circle * self.smooth)
    self.circle = new_circle
    msg = mido.Message('control_change', channel = channel, control = control, value = new_circle)
    self.output.send(msg)
  def send_grid_scores (self, channel, grid_scores):
    """
    Send a Control Change message.

    :param channel: MIDI channel (0-15)
    :param grid_scores
    """
    new_grid = (1.0 - self.smooth) * self.grid + self.smooth * np.array(grid_scores)

    self.grid = new_grid
    for i in range(1, len(new_grid) + 1):
      msg = mido.Message('control_change', channel = channel, control = i, value = int(new_grid[i-1]))
      self.output.send(msg)

  def send_program_change (self, channel, program):
    """
    Send a Program Change message.

    :param channel: MIDI channel (0-15)
    :param program: Program number (0-127)
    """
    msg = mido.Message('program_change', channel = channel, program = program)
    self.output.send(msg)

