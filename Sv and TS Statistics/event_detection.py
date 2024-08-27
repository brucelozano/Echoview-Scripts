from typing import List
import echoview as ev
import numpy as np

class Operator(ev.OperatorBase):
    def result_type(self, input_types: List[ev.MeasurementType]):
        # Output type is Boolean for event detection
        return ev.MeasurementType.SINGLE_BEAM_BOOLEAN

    def eval(self, inputs: List[ev.OperandInput]):
        # Retrieve all measurements from the single operand's window
        measurements = inputs[0].window_measurements

        # Assuming each measurement is an array of data points
        if not measurements:
            return np.array([False])  # Ensure always returning something valid

        # Convert the list of measurements to a linear array of backscatter strengths
        linear_data = np.array([10 ** (m.data / 10) for m in measurements])

        # Ensure linear_data is a 2D array (pings x samples)
        if linear_data.ndim == 1:
            linear_data = linear_data[:, np.newaxis]

        # Calculate changes between successive measurements, assumes first dimension is pings
        changes = np.diff(linear_data, axis=0) / linear_data[:-1]

        # Define a threshold for significant increase, e.g., 20% increase
        significant_increase_threshold = 0.2

        # Determine where changes exceed the threshold
        events_detected = (changes > significant_increase_threshold).any(axis=1)

        # Initialize the result array to False for each ping
        result_array = np.zeros(linear_data.shape[0], dtype=bool)
        result_array[1:] = events_detected  # Skip the first as there's no prior ping to compare

        return result_array
