import os
from visuals import Color, PulsingAnimation, MetronomeAnimation, LinearAnimation
from configuration import Configuration


class State:
    """A class representing the state of Mynt."""

    class Animations:
        """All the different animations of Mynt."""

        BLANK = lambda: Color() # Default animation. Does nothing.
        ERROR = PulsingAnimation(Color(0, 0, 0), Color(1, 1, 1), 1) # TODO
        CON_WIFI = MetronomeAnimation(Color(0, 0, 0), 1) # TODO
        CON_SERVER = MetronomeAnimation(Color(0, 0, 0), 1) # TODO

    state_animation = Animations.BLANK

    def __init__(self):
        if not os.path.exists("~/mynt/config.txt"):
            # TODO: ERROR -- no config found, play error animation
            pass
        else:
            self.configuration = Configuration.from_file("~/mynt/config.txt")
        
    def run(self):
        """The main program loop."""

    
if __name__ == "__main__":
    state = State()
    state.run
