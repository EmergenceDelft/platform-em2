import cv2
import numpy as np
import mido
from mido import Message
import math
import time
from midi_sender import MidiSender
from frame_processor import FrameProcessor

def list_midi_ports():
    ports = mido.get_output_names()
    print("Available MIDI Output Ports:")
    for port in ports:
        print(port)
    return ports

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
    frame_processor = FrameProcessor(cap)

    while True:
        # Delay to ensure consistent frame rate
        time.sleep(0.15)  # Adjust delay as needed
        
        ret, current_frame = cap.read()
        if not ret:
            break

        mean_score = frame_processor.mean_score(prev_frame, current_frame)
        grid_scores = frame_processor.compute_grid_difference(prev_frame, current_frame)

        frame_processor.display_difference(prev_frame, current_frame)

        midi_sender.send_control_change(0, 0, int(mean_score/2))
        grid_scores = grid_scores.flatten()
        for i in range(1, 10):
            midi_sender.send_control_change(channel = 0, control = i, value = int(grid_scores[i-1]/2))

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
