import cv2
import numpy as np
import mido
from mido import Message
import math
import time
from midi_sender import MidiSender
from frame_processor import FrameProcessor
import datetime

def list_midi_ports():
    ports = mido.get_output_names()
    print("Available MIDI Output Ports:")
    for port in ports:
        print(port)
    return ports

def normalize_score(score):
    """Get's the score in range (0, 255) and it normalizes it to (0, 127). It applies log scale."""
    # Apply logarithmic scaling to give more weight to smaller changes
    scaled_diff = math.log1p(score)  # log1p(x) = log(1 + x)

    # Normalize the scaled difference to a value between 0 and 4096
    max_log_diff = math.log1p(255)  # log1p(255) is the maximum possible log-scaled difference
    normalized_score = int((scaled_diff / max_log_diff) * 127)
    return int(normalized_score)
def send_means(midi_sender, mean_score, grid_scores):
    midi_sender.send_control_change(0, 0, mean_score)

    for i in range(1, len(grid_scores)+1):
        midi_sender.send_control_change(channel = 0, control = i, value = grid_scores[i - 1])

def process_frame(current_frame, prev_frame, frame_processor):
    # Get difference from the frame
    mean_score = normalize_score(frame_processor.mean_score(prev_frame, current_frame))
    grid_scores = frame_processor.compute_grid_difference(frame_processor.ref_frame, current_frame)
    grid_scores = [normalize_score(s) for s in grid_scores.flatten()]
    frame_processor.display_difference(frame_processor.ref_frame, current_frame)

    # track objects
    #new_frame, obj_counts = frame_processor.detect_people(current_frame)
    #cv2.imshow(new_frame)
    return mean_score, grid_scores, 0
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
    frame_processor = FrameProcessor(cap, num_reg = 2, ref_frame = prev_frame)
    # frame_processor.setup_counter([(10, 10), (10, frame_processor.height-10),
    #                                (frame_processor.width-10, frame_processor.height-10),
    #                                (frame_processor.width-10, 10)])
    start = datetime.datetime.now()

    while True:
        time.sleep(0.04)
        ret, current_frame = cap.read()
        now = datetime.datetime.now()
        total = (now - start).total_seconds()
        #print(total)
        if total > 1:
            print("Detection counts:", object_counts)
            frame_processor.restart_count()
            start = datetime.datetime.now()
        # Blur the frame to get rid of the noise
        current_frame = frame_processor.blur_frame(current_frame, kernel_size = (9,9))
        if not ret:
            break

        mean_score, grid_scores, object_counts = process_frame(current_frame, prev_frame, frame_processor)

        # send the scores through midi
        send_means(midi_sender, mean_score, grid_scores)

        print(f"Mean Difference Score: {mean_score}")
        print(f"Grid Difference Score: {grid_scores}")


        # Update the previous frame
        prev_frame = current_frame.copy()
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    midi_out.close()

if __name__ == "__main__":
    main()
