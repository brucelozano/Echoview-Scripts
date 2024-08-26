from typing import List
import echoview as ev
import numpy as np
import numpy.fft as fft

class Operator(ev.OperatorBase):
    def __init__(self):
        # Initialize necessary parameters
        self.low_freq = 8  # Low cutoff for band-pass filter
        self.high_freq = 16  # High cutoff for band-pass filter
        self.offset = 1e-5  # Small value to ensure logarithmic conversion

    def eval(self, inputs: List[ev.OperandInput]):
        first_input = inputs[0]
        measurement = first_input.measurement
        data = np.copy(measurement.data)

        # Convert dB to linear scale for processing
        data_linear = 10 ** (data / 20)

        # Apply Fourier Transform
        data_fft = fft.fft(data_linear)

        # Create a band-pass filter
        d = len(data_fft)
        filter = np.zeros(d)
        filter[self.low_freq:self.high_freq] = 1
        filter[d-self.high_freq:d-self.low_freq] = 1

        # Apply the filter
        data_fft_filtered = data_fft * filter

        # Apply inverse Fourier Transform
        data_ifft = fft.ifft(data_fft_filtered).real

        # Ensure no negative values before logarithmic conversion
        data_ifft[data_ifft < self.offset] = self.offset

        # Convert back to dB scale
        data_ifft_db = 20 * np.log10(data_ifft)

        return data_ifft_db.astype(np.float32)
