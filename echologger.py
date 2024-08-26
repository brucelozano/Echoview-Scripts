"""
Echoview Code Operator source file
========================================================================

Created by Echoview(R) 10.0.218 on Monday, 29 April 2019

See the Echoview help file for Code operator documentation and
examples.

NumPy User Guide: https://docs.scipy.org/doc/numpy/user/
NumPy Reference: https://docs.scipy.org/doc/numpy/Reference/
SciPy Reference Guide: https://docs.scipy.org/doc/scipy/Reference/

Echoview(R) is a registered trademark of Echoview Software Pty Ltd.
"""

# Authorship information
__author__ = "Echoview Software Pty Ltd. 2019."
__disclaimer__ = (
    "This example code is provided AS IS, without warranty of any "
    "kind, express or implied, including but not limited to the "
    "warranties of merchantability, fitness for a particular purpose "
    "and noninfringement. In no event shall Echoview Software Pty Ltd "
    "be liable for any claim, damages or other liability, arising "
    "from, out of or in connection with the use of this example code."
)
__version__ = "1.0"

# System Imports
from typing import List

# Libraries
from echoview import OperatorBase, MeasurementType, OperandInput, Error
import numpy as np
import logging


class Operator(OperatorBase):
    """
    Demonstrates methods of diagnosing issues in Python code
    ====================================================================

    Operands
    ---------------------

    * Operand 1 - Any acoustic variable

    Notes
    ---------------------

    This example demonstrates a few techniques that can be used to
    diagnose issues with your operators by inspecting their state.
    The approaches outlined here are:

    Logging
    ^^^^^^^^^^^^^^^^^^^^^

    Python provides a complete logging framework that can be used to log
    details about the system to file for later inspection which can be
    useful for diagnosing issues. Note that as the eval method is
    invoked once for every generated ping this can produce a lot of
    messages.

    Exceptions
    ^^^^^^^^^^^^^^^^^^^^^

    Since Echoview will log the **first** exception raised to the
    Message panel this can be used when developing an algorithm to
    inspect the current state of the system. This can be combined with
    a ping guard, demonstrated below, to only inspect a specific ping.
    Please remember to remove these exceptions once done since Echoview
    will generate a no-data ping when an exception is raised (regardless
    of if it's logged or not).
    """

    def __init__(self):
        # Create a logger for this operator instance that logs to the
        # 'echoview.log' file
        self.logger = logging.getLogger('echoview.copy')
        self.logger.setLevel(logging.DEBUG)

        # create file handler for this logger
        fh = logging.FileHandler('echoview.log')
        fh.setLevel(logging.DEBUG)

        # create formatter and add it to the handlers
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)

        # add the handlers to the logger
        self.logger.addHandler(fh)

    def eval(self, inputs: List[OperandInput]):
        # log some details about the input ping to file
        self.logger.info(
            f'Ping {inputs[0].measurement.index}: '
            f'Number of samples = {inputs[0].measurement.data.size}, '
            f'Samples= {inputs[0].measurement.data}')

        # Echoview will report the first exception raised by the
        # operator in it's messages pane. When combined with a ping
        # guard to get the measurement of interest this can be used to
        # inspect the state of the system while developing your
        # algorithms
        if inputs[0].measurement.index == 3:
            raise Error(
                f'Ping 3: '
                f'Number of samples = {inputs[0].measurement.data.size}, '
                f'Samples= {inputs[0].measurement.data}')

        return inputs[0].measurement.data