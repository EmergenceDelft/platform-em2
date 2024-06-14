import cv2
import numpy as np
import mido
from mido import Message
import math
import time

def frame_difference_score(frame1, frame2):
    # Apply Gaussian blur to reduce noise and small changes
    blurred_frame1 = cv2.GaussianBlur(frame1, (21, 21), 0)
    blurred_frame2 = cv2.GaussianBlur(frame2, (21, 21), 0)
    
    # Compute the absolute difference between the blurred frames
    diff = cv2.absdiff(blurred_frame1, blurred_frame2)
    
    # Convert the difference frame to grayscale
    gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    
    # Compute the mean of the grayscale difference
    mean_diff = np.mean(gray_diff)
    
    # Apply logarithmic scaling to give more weight to smaller changes
    scaled_diff = math.log1p(mean_diff)  # log1p(x) = log(1 + x)
    
    # Normalize the scaled difference to a value between 0 and 4096
    max_log_diff = math.log1p(255)  # log1p(255) is the maximum possible log-scaled difference
    normalized_score = int((scaled_diff / max_log_diff) * 4096)
    
    return normalized_score, gray_diff

def send_midi_message(value, midi_out, control=1):
    # Create a MIDI control change message
    msg = Message('control_change', control=control, value=value)
    
    # Send the MIDI message
    midi_out.send(msg)

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
    
    # Specify your MIDI port name
    midi_port_name = 'platform midi Port 1'
    
    # Check if the specified MIDI port is available
    if midi_port_name not in available_ports:
        print(f"Error: MIDI port '{midi_port_name}' not found.")
        return
    
    # Open the specified MIDI output port
    midi_out = mido.open_output(midi_port_name)

    # Parameters for decay
    current_midi_value = 30
    decay_rate = 1  # The rate at which the value decays
    min_midi_value = 10
    
    while True:
        # Delay to ensure consistent frame rate
        time.sleep(0.15)  # Adjust delay as needed
        
        ret, current_frame = cap.read()
        if not ret:
            break
        
        score, gray_diff = frame_difference_score(prev_frame, current_frame)
        print(f"Frame Difference Score: {score}")
        
        # Scale score to a value between min_midi_value and 127 (MIDI velocity range)
        new_midi_value = int((score / 4096.0) * (127 - min_midi_value) + min_midi_value)
        new_midi_value = min(max(new_midi_value, min_midi_value), 127)
        
        if new_midi_value > current_midi_value:
            current_midi_value = new_midi_value
        else:
            current_midi_value = max(current_midi_value - decay_rate, min_midi_value)
        
        send_midi_message(int(current_midi_value), midi_out)
        
        # Display the live video and the grayscale difference
        cv2.imshow('Live Video', current_frame)
        cv2.imshow('Grayscale Difference', gray_diff)
        
        # Update the previous frame
        prev_frame = current_frame.copy()
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    midi_out.close()

if __name__ == "__main__":
    main()
