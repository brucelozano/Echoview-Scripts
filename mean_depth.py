"""
    @author: bruce
"""

from typing import List
import echoview as ev
import numpy as np

"""
    Calculates mean depth of DSLs to Operand 0 and visualizes them in meters on the echogram
    
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
        valid_depths = depths[valid_indices] # Get the deoths that belong to these valid indices
        mean_depth = np.mean(valid_depths) if valid_depths.size > 0 else float('nan')

        # Initialize output array with NaNs to signify missing data where DSL isn't detected
        output_array = np.full_like(sv_data, np.nan, dtype=np.float32)
        
        # If the mean depth is calculated, fill output array up to the index corresponding to the mean depth
        if not np.isnan(mean_depth):
            index_of_mean_depth = np.argmin(np.abs(depths - mean_depth))
            output_array[:index_of_mean_depth] = mean_depth  # Fill up to the mean depth

        return output_array
