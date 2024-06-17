import numpy as np
import cv2
import math

class FrameProcessor:
    def __init__(self, cap):
        self.cap = cap
        self.width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def crop_frame(self, frame):
      # Crop the frames to the largest size divisible by 3
      crop_height = (int)(self.height // 3) * 3
      crop_width = (int)(self.width // 3) * 3

      return frame[:crop_height, :crop_width]

    def blur_frame (self, frame, kernel_size=(5, 5)):
      return cv2.GaussianBlur(frame, kernel_size, 0)

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
        grid_height = int (self.height // 3)
        grid_width = int (self.width // 3)

        # Initialize the difference grid
        diff_grid = np.zeros((3, 3))

        # Compute the difference for each grid square
        for i in range(3):
          for j in range(3):
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
      for i in range(1, 3):
        cv2.line(gray_diff, (0, i * height // 3), (width, i * height // 3), (255, 255, 255), 2)
        cv2.line(gray_diff, (i * width // 3, 0), (i * width // 3, height), (255, 255, 255), 2)

      # Display the difference image with grid lines
      cv2.imshow("Difference with Grid", gray_diff)