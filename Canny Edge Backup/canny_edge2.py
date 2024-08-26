from typing import List
import echoview as ev
import numpy as np
import cv2

class Operator(ev.OperatorBase):
    def __init__(self):
        # Thresholds for Canny edge detection tuned to emphasize DSL characteristics
        self.low_threshold = 100  # Adjust based on results
        self.high_threshold = 150  # Adjust based on results

    def eval(self, inputs: List[ev.OperandInput]):
        first_input = inputs[0]
        ping = first_input.measurement
        ping_copy = np.copy(ping.data)

        # Define the DSL dB range and normalize data accordingly
        min_val, max_val = -70, -65  # Adjust to finely tune DSL emphasis
        ping_copy[ping_copy < min_val] = min_val
        ping_copy[ping_copy > max_val] = min_val  # Flatten out-of-range values

        # Scale the data to 0-255
        scaled_data = ((ping_copy - min_val) / (max_val - min_val)) * 255

        # Apply Gaussian blur with a horizontal kernel to emphasize horizontal features
        kernel_size = (1, 15)  # This kernel spans more horizontally
        blurred_data = cv2.GaussianBlur(scaled_data.reshape(1, -1), kernel_size, 0)

        # Canny edge detection
        canny_data = cv2.Canny(blurred_data.astype(np.uint8), self.low_threshold, self.high_threshold)

        # Apply morphological operations to clean up the edges
        kernel = np.ones((5, 5), np.uint8)
        closed_canny_data = cv2.morphologyEx(canny_data, cv2.MORPH_CLOSE, kernel)

        return closed_canny_data.flatten().astype(np.float32)
