from typing import List
import echoview as ev
import numpy as np

class Operator(ev.OperatorBase):
    def result_type(self, input_types: List[ev.MeasurementType]):
        # The output will be in linear units, but returning as unspecified dB for generic handling in Echoview.
        return ev.MeasurementType.SINGLE_BEAM_UNSPECIFIED_DB

    def eval(self, inputs: List[ev.OperandInput]):
        # Assign operands to Python variables
        sv_operand = inputs[0]
        ts_operand = inputs[1]

        # Convert dB values to linear scale
        sv_linear = 10 ** (sv_operand.measurement.data / 10)
        ts_linear = 10 ** (ts_operand.measurement.data / 10)

        # Calculate the ratio of Sv to TS in linear units
        ratio_linear = sv_linear / ts_linear

        # Return the ratio
        return ratio_linear