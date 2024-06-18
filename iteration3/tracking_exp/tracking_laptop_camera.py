import cv2
import torch
import numpy as np
from ultralytics import YOLO
import datetime


model = YOLO("yolov8n.pt")

# Open the first camera connected to the system
cap = cv2.VideoCapture("top-side.mp4")
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1024)
width = int (cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int (cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(width, height)

# Get class names
classes = model.names


CONFIDENCE_THRESHOLD = 0.3
GREEN = (0, 255, 0)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Codec for the video
out = cv2.VideoWriter('output.avi', fourcc, 30.0, (width, height))

while True:
    # start time to compute the fps
    start = datetime.datetime.now()

    ret, frame = cap.read()



    # if there are no more frames to process, break out of the loop
    if not ret:
        break

    # run the YOLO model on the frame
    detections = model(frame)[0]
    print(detections)

    for data in detections.boxes.data.tolist():
        # extract the confidence (i.e., probability) associated with the detection
        confidence = data[4]

        # filter out weak detections by ensuring the
        # confidence is greater than the minimum confidence
        if float(confidence) > CONFIDENCE_THRESHOLD and classes[data[5]] == 'person':
            # if the confidence is greater than the minimum confidence,
            # draw the bounding box on the frame
            #print(data)
            xmin, ymin, xmax, ymax = int(data[0]), int(data[1]), int(data[2]), int(data[3])
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), GREEN, 2)


    # show the frame to our screen
    cv2.imshow("Frame", frame)
    out.write(frame)

    if cv2.waitKey(1) == ord("q"):
        break

# Release the webcam and close all OpenCV windows
cap.release()
out.release()
cv2.destroyAllWindows()
