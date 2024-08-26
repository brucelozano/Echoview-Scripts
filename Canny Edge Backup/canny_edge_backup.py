from typing import List
import echoview as ev
import numpy as np
import cv2

class Operator(ev.OperatorBase):
    def __init__(self):
        # Adjust these thresholds to more suitable values based on DSL characteristics
        self.low_threshold = 100  # Example lower threshold
        self.high_threshold = 150  # Example higher threshold

    def eval(self, inputs: List[ev.OperandInput]):
        first_input = inputs[0]
        ping = first_input.measurement
        ping_copy = np.copy(ping.data)

        # Normalize and filter data
        min_val, max_val = -70, -65  # Set these based on the expected DSL dB range
        ping_copy[ping_copy < min_val] = min_val
        ping_copy[ping_copy > max_val] = min_val  # Flatten values outside DSL range

        # Scale to 0-255 for Canny
        scaled_data = ((ping_copy - min_val) / (max_val - min_val)) * 255
        blurred_data = cv2.GaussianBlur(scaled_data.reshape(1, -1), (5, 5), 0)

        # Canny edge detection
        canny_data = cv2.Canny(blurred_data.astype(np.uint8), self.low_threshold, self.high_threshold)

        # Optional: Morphological closing to connect gaps in edges
        kernel = np.ones((5,5), np.uint8)  # Adjust kernel size to control effect
        closed_canny_data = cv2.morphologyEx(canny_data, cv2.MORPH_CLOSE, kernel)

        return closed_canny_data.flatten().astype(np.float32)
