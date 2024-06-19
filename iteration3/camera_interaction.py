import cv2
import numpy as np
import mido
from mido import Message
import math
import time
from midi_sender import MidiSender
from frame_processor import FrameProcessor
import datetime

RESTART_DETECTION = 5
REFRESH = 0.1
DETECT = False
BLUR = 9
REG = 2
MOVEMENT_CLIP = (5, 150)
GRID_CLIP = (5, 150)
DEBUG = True
def list_midi_ports():
    ports = mido.get_output_names()
    print("Available MIDI Output Ports:")
    for port in ports:
        print(port)
    return ports

def normalize_score(score, clip = (5, 150)):
    """Get's the score in range (0, 255) applies log scale, normalizes it to (0, 127)."""
    # Apply logarithmic scaling to give more weight to smaller changes
    score = np.clip(score, clip[0], clip[1]) - clip[0]
    scaled_diff = math.log1p(score)  # log1p(x) = log(1 + x)

    # Normalize the scaled difference to a value between 0 and 4096
    max_log_diff = math.log1p(clip[1])  # log1p(255) is the maximum possible log-scaled difference
    normalized_score = int((scaled_diff / max_log_diff) * 127)
    return int(normalized_score)

def send_midi(midi_sender, mean_score, grid_scores, object_counts, center_score, send_max = False, show = True):
    midi_sender.send_control_change(0, 0, mean_score)
    midi_sender.send_control_change(0, len(grid_scores)+1, object_counts)
    midi_sender.send_control_change(0, len(grid_scores) + 2, center_score)

    midi_scores = np.zeros(len(grid_scores))
    if send_max:
        #compute max difference and send 100
        midi_scores[np.argmax(grid_scores)] = 100

    else:
        midi_scores = grid_scores

    for i in range(1, len(grid_scores)+1):
        midi_sender.send_control_change(channel = 0, control = i, value = int(midi_scores[i - 1]))

    if show:
        print(f"Mean Difference Score: {mean_score}")
        print(f"Midi Grid Scores: {grid_scores}")
        print(f"Detection counts: {object_counts}")
        print(f"Center Score: {center_score}\n ------")

def process_frame(current_frame, prev_frame, frame_processor, show=True):
    # Get difference from the frame
    mean_score = normalize_score(frame_processor.mean_score(prev_frame, current_frame), MOVEMENT_CLIP)
    grid_scores = frame_processor.compute_grid_difference(frame_processor.ref_frame, current_frame)
    #print(f"Grid scores", grid_scores)
    grid_scores = [normalize_score(s, GRID_CLIP) for s in grid_scores.flatten()]

    # compute score in the middle
    r = int(frame_processor.height // 6)
    masked_curr, mask = frame_processor.mask_circle(current_frame, r)
    masked_ref, _ = frame_processor.mask_circle(frame_processor.ref_frame, r)
    center_score = normalize_score(frame_processor.compute_diff(masked_ref, masked_curr).sum()/(mask.sum()/255), GRID_CLIP)

    if show:
        frame_processor.display_difference(frame_processor.ref_frame, current_frame, "Grid Difference")
        frame_processor.display_difference(prev_frame, current_frame, "Movement")
        frame_processor.display_difference(masked_ref, masked_curr, "Circle")

    return mean_score, grid_scores, center_score
def main():
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open video source.")
        return
    
    ret, prev_frame = cap.read()
    if not ret:
        print("Error: Could not read frame from video source.")
        return

    # List available MIDI ports
    available_ports = list_midi_ports()
    print(available_ports)
    
    midi_sender = MidiSender('platform midi Port 1')

    # Setup frame processor
    frame_processor = FrameProcessor(cap, blur_kernel = (BLUR, BLUR), num_reg = REG)

    start_det = datetime.datetime.now()
    start_mov = start_det

    while True:
        time.sleep(REFRESH)
        ret, current_frame = cap.read()
        if not ret:
            break
        now = datetime.datetime.now()

        if (now - start_det).total_seconds() > RESTART_DETECTION:
            frame_processor.restart_count()
            start_det = datetime.datetime.now()

        object_counts = 0
        # track objects
        if DETECT:
            new_frame, object_counts = frame_processor.detect_people(current_frame)

        # Blur the frame to get rid of the noise
        current_frame = frame_processor.blur_frame(current_frame)

        mean_score, grid_scores, center_score = process_frame(current_frame, prev_frame, frame_processor, show = DEBUG)

        # send the scores through midi
        send_midi(midi_sender, mean_score, grid_scores, object_counts, center_score, show = DEBUG)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    midi_out.close()

if __name__ == "__main__":
    main()
