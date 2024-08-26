import logging
from typing import List
import echoview as ev
import numpy as np

# Setup logging
logging.basicConfig(filename="D:\\Echoview Projects\\Code Operator Scripts\\speed_over_time_log.txt",
                    filemode='a',
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

        mean_depth = sv_data[0]  # Assuming the first element contains the depth info
        current_time = measurement.datetime
        
        # Logging time in HH:MM:SS format
        logging.info(f"Ping Time: {current_time.time()}, Current Mean Depth: {mean_depth} m")

        # Calculate speed and handle the first ping separately
        if self.previous_depth is None or self.previous_time is None:
            speed = float('nan')  # No previous data to calculate speed
            logging.info("No previous data available, skipping speed calculation for the first ping.")
        else:
            time_change = (current_time - self.previous_time).total_seconds()
            depth_change = mean_depth - self.previous_depth
            speed = depth_change / time_change if time_change > 0 else float('nan')
            logging.info(f"Depth Change: {depth_change} m, Time Change: {time_change} s, Speed: {speed} m/s")

        # Update previous values for the next ping
        self.previous_depth = mean_depth
        self.previous_time = current_time

        # Output speed uniformly for the current ping's column
        output_array = np.full_like(sv_data, speed, dtype=np.float32)
        return output_array

