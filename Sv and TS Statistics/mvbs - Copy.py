from typing import List
import echoview as ev
import numpy as np

class Operator(ev.OperatorBase):
    def result_type(self, input_types: List[ev.MeasurementType]):
        # Define the output type as unspecified dB since we're working with dB values.
        return ev.MeasurementType.SINGLE_BEAM_UNSPECIFIED_DB

    def eval(self, inputs: List[ev.OperandInput]):
        # Assign the Sv operand to a variable
        sv_operand = inputs[0]

        # Extract data arrays from the window measurements
        sv_samples_db = np.array([ping.data for ping in sv_operand.window_measurements])

        # Convert from dB to linear
        sv_samples_linear = np.power(10, np.divide(sv_samples_db, 10))

        # Calculate the mean volume backscatter in linear scale
        mean_sv_linear = np.mean(sv_samples_linear, axis = 0)

        # Convert the mean volume backscatter from linear to dB
        mean_sv_db = np.multiply(np.log10(mean_sv_linear), 10)

        # Return the mean volume backscatter in dB
        return mean_sv_db
