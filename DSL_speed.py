from typing import List
import echoview as ev
import numpy as np
import logging

# Setup logging
logging.basicConfig(filename="D:\\Echoview Projects\\Code Operator Scripts\\DSL_speed_log_two.txt",
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class Operator(ev.OperatorBase):
    def eval(self, inputs: List[ev.OperandInput]):
        first_input = inputs[0]
        measurement = first_input.measurement
        data = measurement.data  # This should be the dB data

        # Estimating vertical shift (simple implementation for concept demonstration)
        vertical_shift_estimate = self.estimate_vertical_shift(data)
        logging.info(f"Estimated Vertical Shift: {vertical_shift_estimate}")

        # Generate an output array based on the estimation
        output_array = np.full_like(data, vertical_shift_estimate, dtype=np.float32)
        return output_array

    def estimate_vertical_shift(self, data):
        # Analyzing data for vertical shifts, example with placeholder logic
        if len(data) > 1:
            max_index = np.argmax(data)
            min_index = np.argmin(data)
            vertical_shift = max_index - min_index  # Estimation of vertical movement
            logging.info(f"Max Index: {max_index}, Min Index: {min_index}, Vertical Shift: {vertical_shift}")
            return vertical_shift
        return 0
