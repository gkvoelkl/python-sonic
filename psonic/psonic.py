import random
import time
import threading

#TODO: Optimize imports
from .samples import Sample
from .synthesizers import BEEP
from .internals.chords import _CHORD_QUALITY
from .internals.scales import _SCALE_MODE

from pythonosc import osc_message_builder  # osc support
from pythonosc import udp_client

__debug = False


## Base Classes ##
class ChordQuality:
    """
    Chord Quality
    """

    def __init__(self, name, inter):
        self.name = name
        self.inter = inter



class Message:
    """
    For sending messages between threads
    """

    def __init__(self):
        self._condition = threading.Condition()

    def cue(self):
        with self._condition:
            self._condition.notifyAll()  # Message to threads

    def sync(self):
        with self._condition:
            self._condition.wait()  # Wait for message


class Fx:
    """
    FX Effects
    """

    def __init__(self, mode, phase=0.24, probability=0, prob_pos=0):
        self.mode = mode
        self.phase = phase
        self.probability = probability
        self.prob_pos = prob_pos

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def in_thread(func):
    """Thread decorator"""
    def wrapper():
        _thread = threading.Thread(target=func)
        _thread.start()

    return wrapper


## Module attributes ##
_current_synth = BEEP


## Module methodes ##
def use_synth(synth):
    global _current_synth
    _current_synth = synth


def synth(
    name, note=None, attack=None, decay=None,
    sustain_level=None, sustain=None, release=None,
    cutoff=None, cutoff_attack=None, amp=None, pan=None):
    parameters = []
    parameter = ''

    if note is not None: parameters.append('note: {0}'.format(note))
    if attack is not None: parameters.append('attack: {0}'.format(attack))
    if cutoff_attack is not None: parameters.append('cutoff_attack: {0}'.format(cutoff_attack))
    if decay is not None: parameters.append('decay: {0}'.format(decay))
    if sustain_level is not None: parameters.append('sustain_level: {0}'.format(sustain_level))
    if sustain is not None: parameters.append('sustain: {0}'.format(sustain))
    if release is not None: parameters.append('release: {0}'.format(release))
    if cutoff is not None: parameters.append('cutoff: {0}'.format(cutoff))

    if amp is not None: parameters.append('amp: {0}'.format(amp))
    if pan is not None: parameters.append('pan: {0}'.format(pan))

    if len(parameters) > 0: parameter = ',' + ','.join(parameters)

    command = 'synth :{0}{1}'.format(name.name, parameter)

    _debug('synth command={}'.format(command))
    synth_server.synth(command)


def play(note, attack=None, decay=None, sustain_level=None, sustain=None, release=None, cutoff=None,
         cutoff_attack=None, amp=None, pan=None):
    parameters = []
    parameter = ''

    if attack is not None: parameters.append('attack: {0}'.format(attack))
    if cutoff_attack is not None: parameters.append('cutoff_attack: {0}'.format(cutoff_attack))
    if decay is not None: parameters.append('decay: {0}'.format(decay))
    if sustain_level is not None: parameters.append('sustain_level: {0}'.format(sustain_level))
    if sustain is not None: parameters.append('sustain: {0}'.format(sustain))
    if release is not None: parameters.append('release: {0}'.format(release))
    if cutoff is not None: parameters.append('cutoff: {0}'.format(cutoff))

    if amp is not None: parameters.append('amp: {0}'.format(amp))
    if pan is not None: parameters.append('pan: {0}'.format(pan))

    if len(parameters) > 0: parameter = ',' + ','.join(parameters)

    command = 'play {0}{1}'.format(note, parameter)

    _debug('play command={}'.format(command))
    synth_server.play(command)


def play_pattern_timed(notes, times, release=None):
    """
    play notes
    :param notes:
    :param times:
    :return:
    """
    if not type(notes) is list: notes = [notes]
    if not type(times) is list: times = [times]

    for t in times:
        for i in notes:
            play(i, release=release)
            sleep(t)


def play_pattern(notes):
    """

    :param notes:
    :return:
    """
    play_pattern_timed(notes, 1)


def sample(sample, rate=None, attack=None, sustain=None, release=None, beat_stretch=None,
           start=None, finish=None, amp=None, pan=None):
    parameters = []
    parameter = ''
    command = ''

    if rate is not None: parameters.append('rate: {0}'.format(rate))
    if attack is not None: parameters.append('attack: {0}'.format(attack))
    if sustain is not None: parameters.append('sustain: {0}'.format(sustain))
    if release is not None: parameters.append('release: {0}'.format(release))
    if beat_stretch is not None: parameters.append('beat_stretch: {0}'.format(beat_stretch))
    if start is not None: parameters.append('start: {0}'.format(start))
    if finish is not None: parameters.append('finish: {0}'.format(finish))
    if amp is not None: parameters.append('amp: {0}'.format(amp))
    if pan is not None: parameters.append('pan: {0}'.format(pan))

    if len(parameters) > 0: parameter = ',' + ','.join(parameters)

    if type(sample) == Sample:
        command = 'sample :{0}{1}'.format(sample.name, parameter)
    else:
        command = 'sample "{0}"{1}'.format(sample, parameter)

    _debug('sample command={}'.format(command))
    synth_server.sample(command)


def sleep(duration):
    """
    the same as time.sleep
    :param duration:
    :return:
    """
    synth_server.sleep(duration)
    _debug('sleep', duration)

def sample_duration(sample):
    """
    Returns the duration of the sample (in seconds)

    :param sample:
    :return: number
    """
    return sample.duration


def one_in(max):
    """
    random function  returns True in one of max cases
    :param max:
    :return: boolean
    """
    return random.randint(1, max) == 1


def chord(root_note, chord_quality):
    """
    Generates a list of notes of a chord

    :param root_note:
    :param chord_quality:
    :return: list
    """
    result = []
    n = root_note

    half_tone_steps = _CHORD_QUALITY[chord_quality]

    for i in half_tone_steps:
        n = n + i
        result.append(n)

    return result


def scale(root_note, scale_mode, num_octaves=1):
    """
    Genarates a liste of notes of scale

    :param root_note:
    :param scale_mode:
    :param num_octaves:
    :return: list
    """
    result = []
    n = root_note

    half_tone_steps = _SCALE_MODE[scale_mode]

    for o in range(num_octaves):
        n = root_note + o * 12
        result.append(n)
        for i in half_tone_steps:
            n = n + i
            result.append(n)

    return result

def run(command):
    synth_server.run(command)

def stop():
    synth_server.stop()

def send_message(message, *parameter):
    synth_server.send_message(message, *parameter)

## Compound classes ##

class Ring:
    """
    ring buffer
    """

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


## Connection classes ##
class SonicPi:
    """
    Communiction to Sonic Pi
    """

    UDP_IP = "127.0.0.1"
    UDP_PORT = 4557
    UDP_PORT_OSC_MESSAGE = 4559
    GUI_ID = 'SONIC_PI_PYTHON'

    RUN_COMMAND = "/run-code"
    STOP_COMMAND = "/stop-all-jobs"

    def __init__(self):
        self.client = udp_client.UDPClient(SonicPi.UDP_IP, SonicPi.UDP_PORT)
        self.client_for_messages = udp_client.UDPClient(SonicPi.UDP_IP, SonicPi.UDP_PORT_OSC_MESSAGE)

    def sample(self, command):
        self.run(command)

    def play(self, command):
        command = 'use_synth :{0}\n'.format(_current_synth.name) + command
        self.run(command)

    def synth(self, command):
        self.run(command)

    def sleep(self, duration):
        time.sleep(duration)

    def run(self, command):
        self.send_command(SonicPi.RUN_COMMAND, command)

    def stop(self):
        self.send_command(SonicPi.STOP_COMMAND)

    def test_connection(self):
        # OSC::Server.new(PORT)
        # abort("ERROR: Sonic Pi is not listening on #{PORT} - is it running?")
        pass

    def send_command(self, address, argument=''):
        msg = osc_message_builder.OscMessageBuilder(address=address)
        msg.add_arg('SONIC_PI_PYTHON')
        if argument != "":
            msg.add_arg(argument)
        msg = msg.build()

        self.client.send(msg)

    def send_message(self,message, *parameters):
        msg = osc_message_builder.OscMessageBuilder(message)
        for p in parameters:
            msg.add_arg(p)
        msg = msg.build()
        self.client_for_messages.send(msg)

class SonicPiNew:
    """
    Communiction to Sonic Pi
    """

    UDP_IP = "127.0.0.1"
    UDP_PORT = 4559

    def __init__(self):
        self.client = udp_client.UDPClient(SonicPiNew.UDP_IP, SonicPiNew.UDP_PORT)
        self.commandServer = SonicPi()
        # x= 'live_loop :py do\n  nv=sync "/SENDOSC"\n  puts nv\n  eval(nv[0])\nend'
        # self.commandServer.run(x)

    def set_OSC_receiver(self, source):
        self.commandServer.run(source)

    def send(self, address, *message):
        msg = osc_message_builder.OscMessageBuilder(address)
        for m in message:
            msg.add_arg(m)
        msg = msg.build()
        self.client.send(msg)

    def sample(self, command):
        self.send(command)

    def play(self, command):
        self.send(command)

    def sleep(self, duration):
        time.sleep(duration)


synth_server = SonicPi()

## system functions ##
def _debug(*allargs):  # simple debug function for working in different environments
    if __debug: print(allargs)


if __name__ == '__main__':
    use_synth(SAW)
    play(C5, amp=2, pan=-1)
