from typing import List
import echoview as ev
import numpy as np

    # Compute the standard deviation of backscatter values across pings
    # Number of pings specified by window size established on Code variable properties page
    # Operand 1 will be single beam data in dB 

class Operator(ev.OperatorBase):
    def result_type(self, input_types: List[ev.MeasurementType]):
        # Define the output type as unspecified dB since we're working with dB values
        return ev.MeasurementType.SINGLE_BEAM_UNSPECIFIED_DB

    def eval(self, inputs: List[ev.OperandInput]):
        # Assign Operand 1 to a Python variable
        first_input = inputs[0]

        # Get the ping sample data from all pings in the window of measurement
        ping_samples_db = [ping.data for ping in first_input.window_measurements]

        # Convert from dB to linear 
        ping_samples_linear = np.power(10, np.divide(ping_samples_db, 10))

        # Compute the standard deviation using axis parameter to calculate std dev across the pings
        std_linear = np.std(ping_samples_linear, axis=0)

        # Convert from linear to dB
        std_db = np.multiply(np.log10(std_linear), 10)

        # Return the standard deviation in dB
        return std_db
