from typing import List
import echoview as ev
import numpy as np

# Calculcate the average difference over a moving window for singke beam data
# Useful for visualizing the average difference between Sv and TS echograms

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
        sv_samples_linear = np.power(10, np.divide(sv_samples_db, 10))
        ts_samples_linear = np.power(10, np.divide(ts_samples_db, 10))

        # Calculate the difference for each ping within the window
        differences_linear = sv_samples_linear - ts_samples_linear

        # Calculate the average difference across the window
        average_difference_linear = np.mean(differences_linear, axis = 0)

        # Convert mean from linear to dB
        average_difference_db = np.multiply(np.log10(average_difference_linear), 10)

        # Return the average difference as an array
        return average_difference_db