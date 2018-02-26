import random
import threading
from .synth_server import (
    SonicPi,
    SonicPiNew,
    use_synth,
)
from .psonic import *
from .notes import *
from .scales import *
from .synthesizers import *
from .effects import *
from .samples import *
from .samples.loops import *
from .samples.ambient import *
from .samples.bass import *
from .samples.drums import *
from .samples.electric import *
from .samples.guitars import *
from .samples.misc import *
from .samples.percussions import *
from .samples.tabla import *
from .samples.vinyl import *
from .internals.chords import *
from .internals.scales import *


def in_thread(func):
    """Thread decorator"""

    def wrapper():
        _thread = threading.Thread(target=func)
        _thread.start()

    return wrapper

class Fx:
    """FX Effects"""

    def __init__(self, mode, phase=0.24, probability=0, prob_pos=0):
        self.mode = mode
        self.phase = phase
        self.probability = probability
        self.prob_pos = prob_pos

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

class Ring:
    """ring buffer"""

    def __init__(self, data):
        self.data = data
        self.index = -1

    def __iter__(self):  # return Iterator
        return self

    def __next__(self):  # return Iterator next element
        self.index += 1
        if self.index == len(self.data):
            self.index = 0
        return self.data[self.index]

    def choose(self):  # random choose
        return random.choice(self.data)

# Not used anywhere
class Message:
    """For sending messages between threads"""

    def __init__(self):
        self._condition = threading.Condition()

    def cue(self):
        with self._condition:
            self._condition.notifyAll()  # Message to threads

    def sync(self):
        with self._condition:
            self._condition.wait()  # Wait for message
