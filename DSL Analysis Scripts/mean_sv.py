"""
    @author: bruce
"""

from typing import List
import echoview as ev
import numpy as np

"""
    Computes the mean Sv of DSLs from Operand 0 and visualizes them in dB on the echogram
    
    Operands
    ----------------------------------------------------------------------------------------
    
    * Operand 0 - Code: Canny edge with feature detection
"""

class Operator(ev.OperatorBase):
    def __init__(self):
        # Initialize necessary variables here
        pass

    def eval(self, inputs: List[ev.OperandInput]):
        first_input = inputs[0]
        measurement = first_input.measurement
        sv_data = measurement.data
        
        # Since our input echogram marks non-DSL areas as 0, we filter these out
        valid_indices = np.where(sv_data != 0)[0]
        
        # Initialize the output array with zeros (or NaNs if preferred)
        output_array = np.zeros_like(sv_data)
        
        if valid_indices.size > 0:
            # Calculate mean Sv only for valid DSL indices
            mean_sv = np.mean(sv_data[valid_indices])
            
            # Apply this mean only to the DSL areas in the output array
            output_array[valid_indices] = mean_sv

        return output_array.astype(np.float32)
