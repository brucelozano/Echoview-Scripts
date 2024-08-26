from typing import List
import echoview as ev
import numpy as np

# Calculates the standard deviation of the difference between Sv and TS echograms
# Helps provide insights into the variability of the difference between the two measurements over a series of pings

class Operator(ev.OperatorBase):
    def result_type(self, input_types: List[ev.MeasurementType]):
        # Set output type to an unspecified single beam dB
        return ev.MeasurementType.SINGLE_BEAM_UNSPECIFIED_DB

    def eval(self, inputs: List[ev.OperandInput]):
        # Assign operands to a Python variable
        first_input = inputs[0]
        second_input = inputs[1]

        # Extract ping samples based on window size (pings) value
        sv_samples_db = np.array([ping.data for ping in first_input.window_measurements])
        ts_samples_db = np.array([ping.data for ping in second_input.window_measurements])

        # Convert from dB to linear
        sv_samples_linear = 10 ** (sv_samples_db / 10)
        ts_samples_linear = 10 ** (ts_samples_db / 10)

        # Calculate the difference for each ping within the window in linear scale
        differences_linear = sv_samples_linear - ts_samples_linear

        # Calculate the standard deviation of these differences
        std_deviation = np.std(differences_linear, axis = 0)

        # Convert the standard deviation from linear to dB
        std_deviation_db = 10 * np.log10(std_deviation)

        # Return the standard deviation in dB as an array
        return std_deviation_db
