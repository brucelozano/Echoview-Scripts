from typing import List
import echoview as ev
import numpy as np

class LayerThicknessOperator(ev.OperatorBase):
    def result_type(self, input_types: List[ev.MeasurementType]):
        # Define the output type as unspecified dB since we're working with dB values.
        return ev.MeasurementType.SINGLE_BEAM_UNSPECIFIED_DB

    def eval(self, inputs: List[ev.OperandInput]):
        # Extract data arrays from the window measurements
        sv_samples_db = [ping.data for ping in inputs[0].window_measurements]
        
        # Depths for the corresponding samples
        depths = np.linspace(inputs[0].measurement.start_depth, inputs[0].measurement.stop_depth, len(sv_samples_db[0]))

        # Convert to a numpy array for consistency
        sv_samples_db = np.array(sv_samples_db)

        # Handle missing data by converting NaNs to zero (if necessary)
        sv_samples_db = np.nan_to_num(sv_samples_db, nan=0.0)

        # Convert from dB to linear
        sv_samples_linear = 10 ** (sv_samples_db / 10)

        # Threshold for detecting DSL in linear scale
        threshold_linear = 10 ** (-70 / 10)  # Example threshold in dB

        # Identify where the Sv exceeds the threshold
        dsl_mask = sv_samples_linear > threshold_linear

        # Calculate thickness for each ping in the window
        layer_thicknesses = []
        for mask in dsl_mask:
            if np.any(mask):
                dsl_depths = depths[mask]
                min_depth, max_depth = dsl_depths.min(), dsl_depths.max()
                thickness = max_depth - min_depth
                layer_thicknesses.append(thickness)
            else:
                layer_thicknesses.append(0)

        # Convert the results to a numpy array
        layer_thicknesses = np.array(layer_thicknesses)

        # Ensure the result is a 1D numpy array with the expected length
        expected_length = len(sv_samples_db[0])
        layer_thicknesses_padded = np.pad(layer_thicknesses, (0, max(0, expected_length - len(layer_thicknesses))), 'constant', constant_values=np.nan)

        return layer_thicknesses_padded[:expected_length]

# Example usage
operator = LayerThicknessOperator()
