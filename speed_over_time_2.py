import logging
from typing import List
import echoview as ev
import numpy as np

# Setup logging
#logging.basicConfig(filename="D:\\Echoview Projects\\Code Operator Scripts\\speed_over_time_log.txt",
 #                   filemode='a',
  #                  format='%(asctime)s - %(levelname)s - %(message)s',
   #                 level=logging.INFO)

class Operator(ev.OperatorBase):
    def __init__(self):
        self.previous_depth = None
        self.previous_time = None
        self.speeds = []  # This will store speed calculations for each ping

    def eval(self, inputs: List[ev.OperandInput]):
        first_input = inputs[0]
        measurement = first_input.measurement
        sv_data = measurement.data

        mean_depth = sv_data[0]  # Assuming the first element contains the depth info
        current_time = measurement.datetime

        # Log current data
        #logging.info(f"Ping Time: {current_time.time()}, Current Mean Depth: {mean_depth} m")

        if self.previous_depth is None or self.previous_time is None:
            #logging.info("No previous data available, skipping speed calculation for the first ping.")
            self.speeds.append(float('nan'))  # Append NaN for the first ping where no speed can be calculated
        else:
            time_change = (current_time - self.previous_time).total_seconds()
            depth_change = mean_depth - self.previous_depth
            speed = depth_change / time_change if time_change > 0 else float('nan')
            #logging.info(f"Depth Change: {depth_change} m, Time Change: {time_change} s, Speed: {speed} m/s")
            self.speeds.append(speed)  # Append calculated speed

        # Update previous values for the next ping
        self.previous_depth = mean_depth
        self.previous_time = current_time

        # Ensure output is a 1D numpy array that matches the length of the input data
        speed_array = np.array(self.speeds + [float('nan')] * (len(sv_data) - len(self.speeds)))
        return speed_array.astype(np.float32)
