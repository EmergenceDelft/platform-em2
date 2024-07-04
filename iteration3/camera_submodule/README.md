# Iteration 3 Camera Submodule
This folder contains camera interaction scripts, those allow for tracking movement and people in the installation space.
* The `setup.py` can be used to setup midi mappings by soloing specific CC.
* The `camera_interaction.py` runs a camera and analyzes the live feed. It outputs 7 midi signals based on the detected movement and people.
* The `frame_processor.py` and `midi_sender.py` work as helper classes for sending processing frames and sending midi signals.

## Setup
This section described parameters that can be adjusted in camera interaction and necessary setups steps before running anything.

### Parameters

* `RESTART_DETECTION = 5`
number of seconds between restarting detection counter
* `REFRESH = 0.04`
  refresh rate, seconds between sampling next frame
* `BLUR = 21` kernel size of blur to remove the noise between frame comparisons
* `CENTER_PARAM = 6` controls size of the center region. Calculated: `frame height / CENTER_PARAM`
* `REG = 2` number of region REG x REG
* Score clips - control how the average score is clipped. Calculated: `clip(score, clip._0, clip._1) - clip._0`
  * `MOVEMENT_CLIP = (1.5, 10)`
  * `GRID_CLIP = (10, 180)`
  * `CIRCLE_CLIP = (0, 40)`
* `DEBUG = True` - change if you want to display video
* `DETECT = False` change if you want to enable detection
* `PORT = 'platform midi Port 1'` - midi port name

### Before running the script
1. Make sure you have all dependencies installed - look into general README.
2. The first run of `camera_interaction.py` it might be necessary to download the model weights `yolov8s.pt`. 

## Camera interaction
### Setting up MIDI mappings

### Running camera interaction
1. Make sure the physical environment is **empty and stable**.
   * There are no objects/people in the initial frame, 
   * All lights are in the same way as during the experience
   * Look at the reference picture below:
2. Run `camera_interaction.py`. 
3. Verify the screens look something like this:
4. Verify in Ableton that the midi signal are being sent.



