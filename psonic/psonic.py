import random
from .samples import Sample
from .synthesizers import SAW
from .notes import C5
from .internals.chords import _CHORD_QUALITY
from .internals.scales import _SCALE_MODE
from .synth_server import (
    SonicPi,
    use_synth,
)

__debug = False

def synth(name, note=None, attack=None, decay=None,
    sustain_level=None, sustain=None, release=None,
    cutoff=None, cutoff_attack=None, amp=None, pan=None):

    arguments = locals()
    parameters = ['{0}: {1}'.format(k, v) for k, v in arguments.items() if v is not None]
    parameter = ''
    if len(parameters) > 0: parameter = ',' + ','.join(parameters)

    command = 'synth :{0}{1}'.format(name.name, parameter)

    _debug('synth command={}'.format(command))
    synth_server.synth(command)

def play(note, attack=None, decay=None,
    sustain_level=None, sustain=None, release=None,
    cutoff=None, cutoff_attack=None, amp=None, pan=None):

    arguments = locals()
    parameters = ['{0}: {1}'.format(k, v) for k, v in arguments.items() if v is not None]
    parameter = ''
    if len(parameters) > 0: parameter = ',' + ','.join(parameters)

    command = 'play {0}{1}'.format(note, parameter)

    _debug('play command={}'.format(command))
    synth_server.play(command)

def play_pattern_timed(notes, times, release=None):
    """play notes
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
    """:param notes:
    :return:
    """
    play_pattern_timed(notes, 1)

def sample(sample, rate=None, attack=None, sustain=None,
	   release=None, beat_stretch=None, start=None,
           finish=None, amp=None, pan=None):

    arguments = locals()
    parameters = ['{0}: {1}'.format(k, v) for k, v in arguments.items() if v is not None]
    parameter = ''
    command = ''

    if len(parameters) > 0: parameter = ',' + ','.join(parameters)
    if type(sample) == Sample:
        command = 'sample :{0}{1}'.format(sample.name, parameter)
    else:
        command = 'sample "{0}"{1}'.format(sample, parameter)

    _debug('sample command={}'.format(command))
    synth_server.sample(command)

def sleep(duration):
    """the same as time.sleep
    :param duration:
    :return:
    """
    synth_server.sleep(duration)
    _debug('sleep', duration)

def sample_duration(sample):
    """Returns the duration of the sample (in seconds)
    :param sample:
    :return: number
    """
    return sample.duration

def one_in(max):
    """random function  returns True in one of max cases
    :param max:
    :return: boolean
    """
    return random.randint(1, max) == 1

def chord(root_note, chord_quality):
    """Generates a list of notes of a chord
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
    """Genarates a liste of notes of scale
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


synth_server = SonicPi()

def _debug(*args):
    if __debug: print(args)


if __name__ == '__main__':
    use_synth(SAW)
    play(C5, amp=2, pan=-1)
