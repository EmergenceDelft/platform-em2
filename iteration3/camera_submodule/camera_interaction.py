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
REFRESH = 0.05

BLUR = 21
CENTER_PARAM = 4.2
REG = 2

MOVEMENT_CLIP = (1.5, 100)
GRID_CLIP = (10, 180)
CIRCLE_CLIP = (7, 60)

DEBUG = True
DETECT = False

PORT = 'IAC Driver Bus 1'

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
    max_log_diff = math.log1p(clip[1] - clip[0])  # log1p(255) is the maximum possible log-scaled difference
    normalized_score = int((scaled_diff / max_log_diff) * 127)
    return int(normalized_score)

def send_midi(midi_sender, mean_score, grid_scores, object_counts, center_score, show = True):
    midi_sender.send_mean_movement(0, 0, mean_score)

    midi_sender.send_circle_score(0, len(grid_scores) + 2, circle = center_score)

    midi_sender.send_grid_scores(channel = 0, grid_scores = grid_scores)

    # send number of people
    object_counts = int(np.clip(object_counts, 0, 10) * 12)
    midi_sender.send_control_change(0, len(grid_scores) + 1, object_counts)


    #print(f"Mean Difference Score: {mean_score}\n ------")
    print(f"Midi Grid Scores: {grid_scores}")
    #print(f"Detection counts: {object_counts}")
    print(f"Center Score: {center_score}\n ------")

def process_frame(current_frame, prev_frame, frame_processor, show=True):
    # Get average movement from the camera
    mean_score = frame_processor.mean_score(prev_frame, current_frame)
    #print("Mean score:", mean_score)
    mean_score = normalize_score(mean_score, MOVEMENT_CLIP)

    # Get average difference in four zones
    grid_scores = frame_processor.compute_grid_difference(frame_processor.ref_frame, current_frame)
    grid_scores = grid_scores.flatten()[::-1]
    #print("Grid scores", grid_scores.flatten())
    grid_scores = [normalize_score(s, GRID_CLIP) for s in grid_scores.flatten()]

    # compute score in the middle
    r = int(frame_processor.height // CENTER_PARAM)
    masked_curr, mask = frame_processor.mask_circle(current_frame, r)
    masked_ref, _ = frame_processor.mask_circle(frame_processor.ref_frame, r)
    center_score = frame_processor.compute_diff(masked_ref, masked_curr).sum()/(mask.sum()/255)
    print("Circle clip score", center_score)
    center_score = normalize_score(center_score, CIRCLE_CLIP)

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
    
    midi_sender = MidiSender(PORT)

    #time.sleep(1)
    # Setup frame processor
    frame_processor = FrameProcessor(cap = cap, num_reg = REG, blur_kernel = (BLUR, BLUR), diff_thresh = 20, ref_frame = prev_frame)

    start_det = datetime.datetime.now()
    start = datetime.datetime.now()
    while True:
        time.sleep(REFRESH)
        ret, current_frame = cap.read()
        if not ret:
            break
        now = datetime.datetime.now()
        #print("Processing time:", (now - start).total_seconds())
        start = datetime.datetime.now()
        if (now - start_det).total_seconds() > RESTART_DETECTION:
            frame_processor.restart_count()
            start_det = datetime.datetime.now()

        if DEBUG:
            cv2.namedWindow("Live feed", cv2.WINDOW_KEEPRATIO)
            cv2.imshow("Live feed", current_frame)
            cv2.resizeWindow("Live feed", 465, 270)

        object_counts = 0
        # track objects
        if DETECT:
            new_frame, object_counts = frame_processor.detect_people(current_frame)
            #print("Object counts:", object_counts)

        # Blur the frame to get rid of the noise
        current_frame = frame_processor.blur_frame(current_frame)

        mean_score, grid_scores, center_score = process_frame(current_frame, prev_frame, frame_processor, show = DEBUG)

        prev_frame = current_frame.copy()
        # send the scores through midi
        send_midi(midi_sender, mean_score, grid_scores, object_counts, center_score, show = DEBUG)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    midi_out.close()

if __name__ == "__main__":
    main()
