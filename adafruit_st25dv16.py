# SPDX-FileCopyrightText: Copyright (c) 2021 Tim Cocks for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
`adafruit_st25dv16`
================================================================================

CircuitPython driver for the I2C EEPROM of the Adafruit ST25DV16 Breakout


* Author(s): Tim Cocks

Implementation Notes
--------------------

**Hardware:**

* `Adafruit ST25DV16K I2C RFID EEPROM Breakout - STEMMA QT / Qwiic <https://www.adafruit.com/product/4701>`_


**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

# * Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
# * Adafruit's Register library: https://github.com/adafruit/Adafruit_CircuitPython_Register
"""

# imports
import time
from micropython import const
from adafruit_24lc32 import *

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_24LC32.git" ### fix me

_MAX_SIZE_I2C = const(0x800) # 16kbits


class ST25DV16(EEPROM_I2C):
    """I2C class for EEPROM.
    :param: ~busio.I2C i2c_bus: The I2C bus the EEPROM is connected to.
    :param: int address: I2C address of EEPROM. Default address is ``0x50``.
    :param: bool write_protect: Turns on/off initial write protection.
    Default is ``False``.
    :param: wp_pin: (Optional) Physical pin connected to the ``WP`` breakout pin.
    Must be a ``digitalio.DigitalInOut`` object.
    """

    # pylint: disable=too-many-arguments
    def __init__(self, i2c_bus, address=0x53, write_protect=False, wp_pin=None):
        from adafruit_bus_device.i2c_device import (  # pylint: disable=import-outside-toplevel
            I2CDevice as i2cdev,
        )

        self._i2c = i2cdev(i2c_bus, address)
        # does that work ?
        # super().__init__(_MAX_SIZE_I2C, write_protect, wp_pin)
        EEPROM.__init__(self, _MAX_SIZE_I2C, write_protect, wp_pin)

