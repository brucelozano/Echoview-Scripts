from typing import List
import echoview as ev
import numpy as np
import datetime
import logging

# Set up logging
filepath = "D:\Echoview Projects\Code Operator Scripts\DSL_speed_log.txt"

logging.basicConfig(filename='DSL_speed_log.txt', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

class Operator(ev.OperatorBase):
    previous_depth = None
    previous_time = None

    def __init__(self):
        # Initialize any necessary variables here
        pass

    def eval(self, inputs: List[ev.OperandInput]):
        first_input = inputs[0]
        measurement = first_input.measurement
        current_depth = measurement.data[0]
        current_time = measurement.datetime

        # Check if current depth is -inf and log it
        if np.isinf(current_depth) and current_depth < 0:
            logging.info(f"Invalid depth value encountered: {current_depth}")
            current_depth = np.nan  # Consider handling this case differently based on your context

        logging.info(f"Current Depth: {current_depth}, Current Time: {current_time}")

        if self.previous_depth is not None and self.previous_time is not None and not np.isnan(self.previous_depth):
            time_difference = (current_time - self.previous_time).total_seconds()
            depth_change = current_depth - self.previous_depth if not np.isnan(current_depth) else np.nan

            if time_difference > 0 and not np.isnan(depth_change):
                rate_of_movement = depth_change / time_difference
            else:
                rate_of_movement = np.nan
                logging.info("Invalid time difference or depth change, setting rate of movement to NaN.")
        else:
            rate_of_movement = np.nan
            logging.info("No valid previous data available, setting initial rate of movement to NaN.")

        self.previous_depth = current_depth
        self.previous_time = current_time

        output_array = np.full_like(measurement.data, rate_of_movement, dtype=np.float32)
        return output_array
