"""
    @author: bruce
"""

from typing import List
import echoview as ev
import numpy as np

class Operator(ev.OperatorBase):
    def eval(self, inputs: List[ev.OperandInput]):
        first_input = inputs[0]  # Assuming there's only one operand, the echogram data
        ping = first_input.measurement
        data = np.copy(ping.data).astype(np.float32)  # Copy data and ensure it's in float format

        # Handling NaN values by replacing them with zeros for FFT processing
        np.nan_to_num(data, copy=False, nan=0)

        # Compute the FFT
        fft_data = np.fft.fft(data)
        fft_shift = np.fft.fftshift(fft_data)  # Shift zero frequency to center
        
        # Since FFT outputs complex numbers, we might want to visualize the magnitude
        magnitude_spectrum = np.abs(fft_shift)

        # Normalize the magnitude to the 0-255 range for better visualization in Echoview
        normalized_magnitude = np.interp(magnitude_spectrum, (magnitude_spectrum.min(), magnitude_spectrum.max()), (0, 255))
        
        return normalized_magnitude.astype(np.float32)