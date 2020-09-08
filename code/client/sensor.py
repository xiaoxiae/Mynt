"""A module for handling sensor data."""
import asyncio


class Sensor:
    """A class for working with the heartbeat sensor."""

    checked: bool = False  # is toggled when a beat is registered via the check function
    check_frequency: float = 50  # how frequently to check (per second)

    def __init__(self):
        pass  # TODO: init

    def did_a_beat(self):
        """Return True if the sensor detected a beat we haven't processed yet."""
        result = self.checked
        self.checked = False
        return result

    async def check(self):
        while True:
            await asyncio.sleep(1 / self.check_frequency)

            if False:  # TODO: stuff with checking the sensor values
                self.checked = True
