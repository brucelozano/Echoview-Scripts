from typing import List
import echoview as ev
import numpy as np

# Returns a binary output based on a threshold difference between Sv and TS echograms
# Useful for isolating regions in the data where one measurement outnumbers the other

class Operator(ev.OperatorBase):
    def result_type(self, input_types: List[ev.MeasurementType]):
        # Set the output type as boolean since we're working with a threshold-based comparison
        return ev.MeasurementType.SINGLE_BEAM_BOOLEAN

    def eval(self, inputs: List[ev.OperandInput]):
        # Assign operands to a Python variable
        first_input = inputs[0]
        second_input = inputs[1]

        # Extract measurement data
        sv_data = first_input.measurement.data
        ts_data = second_input.measurement.data

        # Convert from dB to linear
        sv_linear = 10 ** (sv_data / 10)
        ts_linear = 10 ** (ts_data / 10)

        # Calculate the difference in linear scale
        difference_linear = sv_linear - ts_linear

        # Define the threshold for comparison in linear scale
        threshold_dB = -2  # Adjust threshold as needed
        threshold_linear = 10 ** (threshold_dB / 10)

        # Compare the difference against the threshold
        result = difference_linear > threshold_linear

        # Return the result as a boolean array
        return result
