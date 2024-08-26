import logging
from typing import List
import echoview as ev
import numpy as np

logging.basicConfig(filename="D:\\Echoview Projects\\Code Operator Scripts\\speed_log.txt",
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

class Operator(ev.OperatorBase):
    def __init__(self):
        self.previous_depth = None
        self.previous_time = None

    def eval(self, inputs: List[ev.OperandInput]):
        first_input = inputs[0]
        measurement = first_input.measurement
        sv_data = measurement.data

        # Extract the depths where the DSL is significant (non-zero)
        depths = np.linspace(measurement.start_depth, measurement.stop_depth, len(sv_data))
        valid_indices = sv_data != 0
        valid_depths = depths[valid_indices]

        logging.info(f"Number of valid depth points: {np.sum(valid_indices)}")

        # Calculate the mean depth of the DSL for the current ping
        current_depth = np.mean(valid_depths) if valid_depths.size > 0 else None
        current_time = measurement.datetime

        logging.info(f"Current mean DSL depth: {current_depth}")
        logging.info(f"Current time: {current_time}")
        logging.info(f"Previous time: {self.previous_time}")

        if self.previous_depth is not None and self.previous_time is not None and current_depth is not None:
            time_change = (current_time - self.previous_time).total_seconds()
            logging.info(f"Time change is: {time_change} seconds")
            depth_change = current_depth - self.previous_depth
            logging.info(f"Depth change is: {depth_change} meters")
            if time_change > 0:
                speed = abs(depth_change / time_change)
            else:
                speed = float('nan')
                logging.warning("Time change is zero, speed set to NaN")
        else:
            speed = float('nan')  # Handling the first ping or missing data
            logging.info("First ping or missing data, speed set to NaN")

        # Prepare the output array
        output_array = np.full_like(sv_data, speed, dtype=np.float32)  # Fill the entire ping with the calculated speed

        logging.info(f"Output array shape: {output_array.shape}")

        # Update for next ping
        self.previous_depth = current_depth
        self.previous_time = current_time

        logging.info("Evaluation complete")

        return output_array.astype(np.float32)
