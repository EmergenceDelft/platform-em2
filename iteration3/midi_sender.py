import mido

class MidiSender:
  def __init__ (self, port_name=None):
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

  def open_port (self):
    """
    Open the MIDI port for sending messages.
    """
    if self.port_name:
      self.output = mido.open_output(self.port_name)
    else:
      self.output = mido.open_output()

  def close_port (self):
    """
    Close the MIDI port.
    """
    if self.output:
      self.output.close()
      self.output = None

  def send_note_on (self, channel, note, velocity):
    """
    Send a Note On message.

    :param channel: MIDI channel (0-15)
    :param note: MIDI note number (0-127)
    :param velocity: Note velocity (0-127)
    """
    msg = mido.Message('note_on', channel = channel, note = note, velocity = velocity)
    self.output.send(msg)

  def send_note_off (self, channel, note, velocity):
    """
    Send a Note Off message.

    :param channel: MIDI channel (0-15)
    :param note: MIDI note number (0-127)
    :param velocity: Note velocity (0-127)
    """
    msg = mido.Message('note_off', channel = channel, note = note, velocity = velocity)
    self.output.send(msg)

  def send_control_change (self, channel, control, value):
    """
    Send a Control Change message.

    :param channel: MIDI channel (0-15)
    :param control: Control number (0-127)
    :param value: Control value (0-127)
    """
    msg = mido.Message('control_change', channel = channel, control = control, value = value)
    self.output.send(msg)

  def send_program_change (self, channel, program):
    """
    Send a Program Change message.

    :param channel: MIDI channel (0-15)
    :param program: Program number (0-127)
    """
    msg = mido.Message('program_change', channel = channel, program = program)
    self.output.send(msg)

