"""
    @author: bruce
"""

from typing import List
import echoview as ev
import numpy as np

"""
    Computes vertical extents over time of DSLs from Operand 0 and visualizes them in meters 
    on the echogram
    
    Operands
    ----------------------------------------------------------------------------------------
    
    * Operand 0 - Code: Canny edge with feature detection
"""

class Operator(ev.OperatorBase):
    def __init__(self):
        # Initialize any necessary variables here
        pass

    def eval(self, inputs: List[ev.OperandInput]):
        first_input = inputs[0]
        measurement = first_input.measurement
        sv_data = measurement.data

        # Create an array of depths that correspond to each sample in the echogram
        depths = np.linspace(measurement.start_depth, measurement.stop_depth, len(sv_data))

        valid_indices = sv_data != 0 # Identify indices where Sv data is non-zero
        output_array = np.full_like(sv_data, np.nan, dtype=np.float32)  # Initialize all to NaN

        if any(valid_indices):
            min_depth_index = np.min(np.where(valid_indices)[0])
            max_depth_index = np.max(np.where(valid_indices)[0])

            # Extract the depth range, flatten it to 1D, and assign it back to the output array
            depth_range = depths[min_depth_index:max_depth_index + 1]  # Extract depth range including the max depth
            output_array[min_depth_index:max_depth_index + 1] = depth_range.flatten()  # Assign flattened range

        return output_array
