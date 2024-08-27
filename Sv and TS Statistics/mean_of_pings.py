from typing import List
import echoview as ev
import numpy as np

    # Compute the mean along the ping axis of an echogram
    # Number of pings specified by window size established on Code variable properties page
    # Operand 1 will be single beam data in dB

class Operator(ev.OperatorBase):
    def eval(self, inputs: List[ev.OperandInput]):
        # Assign Operand 1 to a Python variable
        first_input = inputs[0]

        # Get the ping sample data from all pings in the window of measurement (5)
        ping_samples_db = [ping.data for ping in first_input.window_measurements]

        # Convert from dB to linear 
        ping_samples_linear = np.power(10, np.divide(ping_samples_db, 10))

        # Compute the mean using axis parameter to average the pings
        mean_linear = np.mean(ping_samples_linear, axis=0)

        # Convert from linear to dB
        mean_db = np.multiply(np.log10(mean_linear), 10)

        # Return the mean in dB
        return mean_db