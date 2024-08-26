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
        sv_samples_db = [ping.data for ping in sv_operand.window_measurements]

        # Determine the maximum length of data arrays
        max_length = max(len(ping) for ping in sv_samples_db)

        # Pad shorter arrays with zeros to ensure consistent length
        sv_samples_db_padded = np.array([np.pad(ping, (0, max_length - len(ping)), 'constant', constant_values=np.nan) for ping in sv_samples_db])

        # Handle missing data by converting NaNs to zero
        sv_samples_db_padded = np.nan_to_num(sv_samples_db_padded, nan=0.0)

        # Convert from dB to linear
        sv_samples_linear = 10 ** (sv_samples_db_padded / 10)

        # Calculate the mean volume backscatter in linear scale
        mean_sv_linear = np.mean(sv_samples_linear, axis=0)

        # Convert the mean volume backscatter from linear to dB
        mean_sv_db = 10 * np.log10(mean_sv_linear)

        # Ensure the result is a 1D numpy array
        return mean_sv_db
