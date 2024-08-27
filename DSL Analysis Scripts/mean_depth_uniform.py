"""
    @author: bruce
"""

from typing import List
import echoview as ev
import numpy as np

"""
    Calculates mean depth of the DSL from Operand 0 and visualizes them (uniform visual)
    
    Operands
    ----------------------------------------------------------------------------------------
    
    * Operand 0 - Code: Canny edge with feature detection
"""

class Operator(ev.OperatorBase):
    def __init__(self):
        # Initialize any necessary variables here
        pass

    def eval(self, inputs: List[ev.OperandInput]):
        # Access the input data from the first operand
        first_input = inputs[0]
        
        # Get the measurement from the first operand input, which contains the echogram data
        measurement = first_input.measurement
        
        # Retrieve the Sv data, which should be a 1D numpy array of Sv values
        sv_data = measurement.data
        
        # Retrieve depth information for each sample in the ping
        # Assuming depth for each sample is stored in a similar 1D array or can be calculated
        depths = np.linspace(measurement.start_depth, measurement.stop_depth, len(sv_data))

        # Filter to get depths where Sv data indicates DSL presence (non-zero values)
        valid_indices = sv_data != 0
        valid_depths = depths[valid_indices]

        # Calculate the mean depth from valid depths
        mean_depth = np.mean(valid_depths) if valid_depths.size > 0 else float('nan')

        # Prepare the output - assuming the output should also be a single value repeated across the array
        output_array = np.full_like(sv_data, mean_depth, dtype=np.float32)

        return output_array