from typing import List
import echoview as ev
import numpy as np

# Calculate the intensity difference at 1 ping per sample for Sv and TS echograms 
# Useful for providing insight in the difference between intensities belonging to Sv and TS echograms

class Operator(ev.OperatorBase):
    def result_type(self, input_types: List[ev.MeasurementType]):
        # # Set output type to an unspecified single beam dB
        return ev.MeasurementType.SINGLE_BEAM_UNSPECIFIED_DB

    def eval(self, inputs: List[ev.OperandInput]):
        # Assigns Operands to a Python variable
        first_input = inputs[0]
        second_input = inputs[1]

        # Directly accessing the measurement data since our window size is 1
        sv_data = first_input.measurement.data
        ts_data = second_input.measurement.data

        # Calculate the intensity difference for the current ping
        intensity_difference = sv_data - ts_data

        # Return the intensity difference as an array
        return intensity_difference