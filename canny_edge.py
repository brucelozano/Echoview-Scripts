"""
    @author: bruce
"""

from typing import List
import echoview as ev
import numpy as np
import cv2

"""
    Applies Canny edge detection to Operand 0
    
    Operands
    ----------------------------------------------------------------------------------------
    
    * Operand 0 - 18 kHz Whole Water Column Single-beam data. 
"""

class Operator(ev.OperatorBase):
    def __init__(self):
        # Adjust these thresholds to more suitable values based on DSL characteristics
        self.low_threshold = 100  
        self.high_threshold = 150  
        self.dsl_depth_range = (350, 600)  # Depth range in meters where DSLs are expected

    def result_type(self, input_types: List[ev.MeasurementType]):
        # Set output type to an unspecified single beam dB
        return ev.MeasurementType.UNDEFINED

    def eval(self, inputs: List[ev.OperandInput]):
        first_input = inputs[0]
        ping = first_input.measurement
        ping_copy = np.copy(ping.data)

        # Keeping it at 0.135 ensure we iterate through all depths in the DSL range
        depth_per_sample = 0.135 # This value is essentially the range between one sample to another within a ping

        # Normalize and filter data based on depth range to focus on the potential DSL regions
        for i in range(len(ping_copy)):
            depth = i * depth_per_sample
            # Check if depth falls within any part of the DSL range
            if depth + depth_per_sample < self.dsl_depth_range[0] or depth > self.dsl_depth_range[1]:
                ping_copy[i] = -999

        # DSL intensity range
        min_val, max_val = -70, -65 
        ping_copy[ping_copy < min_val] = min_val
        ping_copy[ping_copy > max_val] = min_val

        # Scale to 0-255 for Canny edge detection
        scaled_data = ((ping_copy - min_val) / (max_val - min_val)) * 255
        blurred_data = cv2.GaussianBlur(scaled_data.reshape(1, -1), (1, 15), 0)

        # Canny edge detection
        canny_data = cv2.Canny(blurred_data.astype(np.uint8), self.low_threshold, self.high_threshold)

        # Morphological closing to connect gaps in edges
        kernel = np.ones((5,5), np.uint8)
        closed_canny_data = cv2.morphologyEx(canny_data, cv2.MORPH_CLOSE, kernel)

        return closed_canny_data.flatten().astype(np.float32)