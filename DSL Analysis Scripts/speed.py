"""
    @author: bruce
"""

from typing import List
import echoview as ev
import numpy as np

"""
    Computes the speed of the DSL and outputs results in the shape of the DSL
    
    Operands
    ----------------------------------------------------------------------------------------
    
    * Operand 0 - Code: Mean depth
    * Operand 1 - Code: Canny edge with feature detection
"""

class Operator(ev.OperatorBase):
    def __init__(self):
        # Create dictionary to store ping data
        self.ping_data = {}

    def eval(self, inputs: List[ev.OperandInput]):
        # Get first input (Mean depth)
        first_input = inputs[0]
        # Get second input (Canny Edge with feature detection)
        second_input = inputs[1]
        dsl_shape = second_input.measurement
        dsl_data = dsl_shape.data
        measurement = first_input.measurement
        sv_data = measurement.data

        # Get time and depth from the first input
        current_time = measurement.datetime
        current_depth = np.mean(sv_data)  

        # Store current ping's time and depth where we use the time as our key and depth as our value
        self.ping_data[current_time] = current_depth

        # Sort dictionary and get current index
        sorted_times = sorted(self.ping_data.keys())
        current_index = sorted_times.index(current_time)

        # Speed calculation logic
        if current_index > 0:
            previous_time = sorted_times[current_index - 1]
            previous_depth = self.ping_data[previous_time]

            time_change = (current_time - previous_time).total_seconds()
            depth_change = current_depth - previous_depth
            speed = depth_change / time_change if time_change > 0 else float('NaN')
        else:
            speed = float('NaN')  # No previous ping to compare with

        # Fill output array with the calculated speed for each sample in the ping using the DSL shape as our output shape
        output_array = np.where(dsl_data != 0, speed, float('NaN'))

        return output_array
