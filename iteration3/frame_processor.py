import numpy as np
import cv2
import math
from ultralytics import YOLO, solutions

class FrameProcessor:
    def __init__(self, cap, num_reg, ref_frame = None, conf_tresh = 0.4):
        self.cap = cap
        self.width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.model = YOLO("yolov8n.pt")
        self.num_reg = num_reg
        self.regions = self.get_regions(num_reg, self.width, self.height)
        if ref_frame is None:
          _, self.ref_frame = cap.read()
        else:
          self.ref_frame = ref_frame
        self.count = 0
        self.conf_tresh = conf_tresh
        print("Frame regions: ", self.regions)

    def get_regions(self, number, width, height):
      # Calculate the size of each region
      region_width = width // number
      region_height = height // number

      # List to store the coordinates of each region
      regions = []

      # Iterate over each region and calculate its coordinates
      for i in range(number):
        for j in range(number):
          x1 = j * region_width
          y1 = i * region_height
          x2 = x1 + region_width
          y2 = y1 + region_height
          regions.append(((x1, y1), (x1, y2), (x2, y2), (x2, y1)))

      return regions

    def setup_counter(self, region):
      # setup region counter
      self.counter = solutions.ObjectCounter(
        view_img = True,
        reg_pts = region,
        classes_names = self.model.names,
        draw_tracks = True,
        line_thickness = 2,
      )
      self.restart_count()

    def restart_count(self):
      self.count = 0

    def crop_frame(self, frame):
      # Crop the frames to the largest size divisible by 3
      crop_height = (int)(self.height // self.num_reg) * self.num_reg
      crop_width = (int)(self.width // self.num_reg) * self.num_reg

      return frame[:crop_height, :crop_width]

    def blur_frame (self, frame, kernel_size=(5, 5)):
      return cv2.GaussianBlur(frame, kernel_size, 0)

    def detect_people(self, frame):
      detections = self.model(frame)[0]
      detected = frame
      temp_count = 0
      for data in detections.boxes.data.tolist():
        # extract the confidence (i.e., probability) associated with the detection
        confidence = data[4]

        # filter out weak detections by ensuring the
        # confidence is greater than the minimum confidence and the detected obj is a person
        if float(confidence) > self.conf_tresh and data[5] == 0:
          # if the confidence is greater than the minimum confidence,
          # draw the bounding box on the frame
          temp_count = temp_count+1
          xmin, ymin, xmax, ymax = int(data[0]), int(data[1]), int(data[2]), int(data[3])
          #cv2.rectangle(detected, (xmin, ymin), (xmax, ymax), (255, 0, 0), 2)

      self.count = max(self.count, temp_count)
      return detected, self.count

    def compute_diff(self, frame1, frame2):
      diff = cv2.absdiff(frame1, frame2)
      gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
      return gray_diff

    def compute_grid_difference(self, frame1, frame2):
        """
        Compute the absolute difference between two frames divided into a 3x3 grid.

        :param frame1: First frame as a NumPy array.
        :param frame2: Second frame as a NumPy array.
        :return: A 3x3 NumPy array containing the differences for each grid square.
        """

        frame1_cropped = self.crop_frame(frame1)
        frame2_cropped = self.crop_frame(frame2)

        diff = self.compute_diff(frame1_cropped, frame2_cropped)

        # Compute the size of each grid square
        grid_height = int (self.height // self.num_reg)
        grid_width = int (self.width // self.num_reg)

        # Initialize the difference grid
        diff_grid = np.zeros((self.num_reg, self.num_reg))

        # Compute the difference for each grid square
        for i in range(self.num_reg):
          for j in range(self.num_reg):
            square = diff[i * grid_height:(i + 1) * grid_height, j * grid_width:(j + 1) * grid_width]
            diff_grid[i, j] = np.mean(square)

        return diff_grid

    def mean_score (self, frame1, frame2):
      # Compute the absolute difference between the frames
      diff = self.compute_diff(frame1, frame2)

      # Compute the mean of the grayscale difference
      mean_diff = np.mean(diff)

      return mean_diff

    def display_difference (self, frame1, frame2):
      """
      Display the difference between two frames with a 3x3 grid overlay.

      :param frame1: First frame as a NumPy array.
      :param frame2: Second frame as a NumPy array.
      """
      frame1_cropped = self.crop_frame(frame1)
      frame2_cropped = self.crop_frame(frame2)

      # Convert the difference frame to grayscale
      gray_diff = self.compute_diff(frame1_cropped, frame2_cropped)

      height, width = gray_diff.shape

      # Draw the grid lines
      for i in range(1, self.num_reg):
        cv2.line(gray_diff, (0, i * height // self.num_reg), (width, i * height // self.num_reg), (255, 255, 255), 2)
        cv2.line(gray_diff, (i * width // self.num_reg, 0), (i * width // self.num_reg, height), (255, 255, 255), 2)

      # Display the difference image with grid lines
      cv2.imshow("Difference with Grid", gray_diff)