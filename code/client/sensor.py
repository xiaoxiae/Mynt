"""A module for handling sensor data."""
import asyncio

import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn


class Sensor:
    """A class for working with the heartbeat sensor."""

    checked: bool = False  # is toggled when a beat is registered via the check function
    check_frequency: float = 50  # how frequently to check (per second)

    def __init__(self):
        pass # TODO: initialize the sensors; something like:
             # i2c = busio.I2C(board.SCL, board.SDA)
             # ads = ADS.ADS1015(i2c)

             # # Create single-ended input on channel 0
             # chan = AnalogIn(ads, ADS.P0)

             # # Create differential input between channel 0 and 1
             # #chan = AnalogIn(ads, ADS.P0, ADS.P1)

             # while True:
             #     print(chan.value, chan.voltage)


    def check(self):
        """Return True if the sensor detected a beat we haven't processed yet."""
        result = self.checked
        self.checked = False
        return result

    async def periodic_check(self):
        """An asynchronous function that checks for values from ADS and stores them in
        a variable."""
        while True:
            await asyncio.sleep(1 / self.check_frequency)

            if False:  # TODO: stuff with checking the sensor values
                self.checked = True

if __name__ == "__main__":


    
