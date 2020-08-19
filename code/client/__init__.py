import os
from visuals import Color, PulsingAnimation, MetronomeAnimation, LinearAnimation
from configuration import ConfigurationWatcher


class State:
    """A class representing the state of Mynt."""

    class Animations:
        """All the different animations of Mynt."""

        BLANK = lambda: Color(0, 0, 0)
        ERROR = PulsingAnimation(Color(0, 0, 0), Color(1, 1, 1), 1)  # TODO
        CONNECTING_TO_WIFI = MetronomeAnimation(Color(0, 0, 0), 1)  # TODO
        CONNECTING_TO_SERVER = MetronomeAnimation(Color(0, 0, 0), 1)  # TODO

    state_animation = Animations.BLANK

    def __init__(self):
        self.cw = ConfigurationWatcher()

    def run(self):
        """The main program loop. Runs around 60 times per second."""

        # TODO: LEDs
        # TODO: communication with the server

        if self.cw.changed():
            if self.cw.configuration is None:
                pass  # TODO: error animation


if __name__ == "__main__":
    state = State()
    state.run
