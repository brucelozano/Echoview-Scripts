from typing import List
import echoview as ev
import numpy as np

class Operator(ev.OperatorBase):
    def __init__(self):
        # Initialize any necessary variables here
        pass

    def eval(self, inputs: List[ev.OperandInput]):
        first_input = inputs[0]
        measurement = first_input.measurement
        sv_data = measurement.data
        depths = np.linspace(measurement.start_depth, measurement.stop_depth, len(sv_data))
        valid_indices = sv_data != 0
        
        output_array = np.full_like(sv_data, np.nan, dtype=np.float32)  # Set all to NaN initially

        if any(valid_indices):
            min_depth_index = np.min(np.where(valid_indices)[0])
            max_depth_index = np.max(np.where(valid_indices)[0])
            output_array[min_depth_index] = depths[min_depth_index]
            output_array[max_depth_index] = depths[max_depth_index]

        return output_array
