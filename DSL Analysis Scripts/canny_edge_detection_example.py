from typing import List
import echoview as ev
import numpy as np
import cv2

class Operator(ev.OperatorBase):
    """
    Applies Canny edge detection to operand 0.
    
    Operands
    ----------------------------------------------------------------------------------------
    
    * Operand 0 - Smoothed multibeam data.
    
    """
    
    def __init__(self):
        # Define thresholds for Canny edge detection
        self.low_threshold = 70
        self.high_threshold = 120
    
    def eval(self, inputs: List[ev.OperandInput]):
        
        # Access the input ping of operand 0
        first_input = inputs[0]

        # Access the matched ping
        ping = first_input.measurement
        
        # Create copy of data in matched ping (ping.data is read-only)
        ping_copy = np.copy(ping.data)
        
        # Replace -inf values with 0.0
        ping_copy[ping_copy == float('-inf')] = 0.0
        
        # Scale data values to 0-255
        scaled_data = ((ping_copy - np.min(ping_copy))
                        / (np.max(ping_copy) - np.min(ping_copy)) * 255)
        
        # Apply canny edge detection to scaled data
        canny_data = cv2.Canny(scaled_data.astype(np.uint8),
                               self.low_threshold, self.high_threshold)
        
        return canny_data.astype(np.float32)