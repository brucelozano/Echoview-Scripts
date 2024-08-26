from typing import List
import echoview as ev
import numpy as np

class Operator(ev.OperatorBase):
    def __init__(self):
        # Initialize any necessary variables here
        pass

    def eval(self, inputs: List[ev.OperandInput]):
        # Access the input data from the first operand
        first_input = inputs[0]
        
        # Get the measurement from the first operand input, which contains the echogram data
        measurement = first_input.measurement
        
        # Retrieve the data, which should be a 1D numpy array of Sv values
        sv_data = measurement.data
        
        # Filter out the zero values which are used to mark non-DSL areas
        valid_sv_data = sv_data[sv_data != 0]  # Exclude 0.00 dB values

        # Calculate the mean Sv value from valid data points
        mean_sv = np.mean(valid_sv_data) if valid_sv_data.size > 0 else float('nan')

        # Create an output array filled with the mean Sv, matching the input array's shape
        output_array = np.full_like(sv_data, mean_sv, dtype=np.float32)

        # Return the output array
        return output_array
