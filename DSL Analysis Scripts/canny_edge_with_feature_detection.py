"""
    @author: bruce
"""

from typing import List
import echoview as ev
import numpy as np
import cv2

"""
    Applies Canny edge detection to Operand 0 and finds contours to extract features from DSL
    
    Operands
    ----------------------------------------------------------------------------------------
    
    * Operand 0 - 18 kHz Whole Water Column Single-beam data.
"""

class Operator(ev.OperatorBase):
    def __init__(self):
        # Adjust these thresholds for Canny Edge detection
        self.low_threshold = 50
        self.high_threshold = 150
        self.dsl_depth_range = (350, 525)  # Depth range in meters where DSLs are expected

    def eval(self, inputs: List[ev.OperandInput]):
        first_input = inputs[0]
        ping = first_input.measurement
        original_data = np.copy(ping.data)  # Preserve original data for final masking
        ping_copy = np.copy(ping.data)

        # Keeping it at 0.135 ensures better iteration through all depths against the DSL range
        depth_per_sample = 0.135

        # Normalize and filter data based on depth range to focus on potential DSL regions
        for i in range(len(ping_copy)):
            depth = i * depth_per_sample
            if depth + depth_per_sample < self.dsl_depth_range[0] or depth > self.dsl_depth_range[1]:
                ping_copy[i] = -999

        min_val, max_val = -70, -65
        ping_copy[ping_copy < min_val] = min_val
        ping_copy[ping_copy > max_val] = min_val

        # Scale to 0-255 for Canny edge detection
        scaled_data = ((ping_copy - min_val) / (max_val - min_val)) * 255
        blurred_data = cv2.GaussianBlur(scaled_data.reshape(1, -1), (1, 15), 0)

        # Canny edge detection
        canny_data = cv2.Canny(blurred_data.astype(np.uint8), self.low_threshold, self.high_threshold)

        # Create custom kernels
        kernel_close = cv2.getStructuringElement(cv2.MORPH_RECT, (120,120))
        kernel_open = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (20,20))
       
        # Morphological closing to connect gaps in edges
        closed_canny_data = cv2.morphologyEx(canny_data, cv2.MORPH_CLOSE, kernel_close)
        opened_canny_data = cv2.morphologyEx(closed_canny_data, cv2.MORPH_OPEN, kernel_open)
        
        # Find contours from the edge-detected image
        contours, _ = cv2.findContours(opened_canny_data, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Create an output mask to draw the detected DSLs
        mask = np.zeros_like(opened_canny_data)
        cv2.drawContours(mask, contours, -1, (255), thickness=cv2.FILLED)

        # Dilation to broaden the mask areas
        dilated_mask = cv2.dilate(mask, np.ones((120, 120), np.uint8), iterations=1)

        # Apply mask to the original data to extract DSL regions
        masked_data = np.where(dilated_mask.flatten() == 255, original_data, 0)

        return masked_data.astype(np.float32)