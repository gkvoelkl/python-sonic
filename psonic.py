import random
import time

import sys

from pythonosc import osc_message_builder #osc support
from pythonosc import udp_client

__debug = False

## Base Classes ##

class Note:
    """
    Note
    """
    def __init__(self,name,midi):
        self.name = name
        self.midi = midi


class Synth:
    """
    Synthesizer
    """
    def __init__(self,name):
        self.name = name

## Notes ##

C5 = Note('C5',72)
Cs5 = Note('CS5',73)
Db5 = Cs5
D5 = Note('D5',74)
Ds5 = Note('Eb5',75)
Eb5 = Ds5
E5 = Note('Eb5',76)
F5 = Note('F5',77)
Fs5 = Note('Fs5',78)
Gb5 = Fs5
G5 = Note('G5',79)
Gs5 = Note('Gs5',80)
Ab5 = Gs5
A5 = Note('A5',81)
As5 = Note('As5',82)
Bb5 = As5
B5 = Note('B5',83)
C6 = Note('C6',84)

R = Note('rest',0)


## Synthezier ##
DSAW = Synth('dsaw')
TB303 = Synth('tb303')
BLADE = Synth('blade')
PROPHET = Synth('prophet')
SAW = Synth('saw')
BEEP = Synth('beep')
TRI = Synth('tri')

## Scale Mode ##
MINOR_PENTATONIC = "minor pentatonic"

## Module attributes ##
_current_synth = BEEP

## Module methodes ##
def use_synth(synth):
    global _current_synth
    _current_synth = synth


def play(note, attack=0, release=0, cutoff=0, amp=None, pan=None):
    parameters = []
    parameter = ''
    command = ''

    if amp is not None: parameters.append('amp: {0}'.format(amp))
    if pan is not None: parameters.append('pan: {0}'.format(pan))

    if len(parameters)>0: parameter = ',' + ','.join(parameters)

    if type(note) == Note :
        command = 'play :{0}{1}'.format(note.name,parameter)
    else:
        command = 'play {0}{1}'.format(note,parameter)

    command = 'use_synth :{0}\n'.format(_current_synth.name) + command
    _debug('play command={}'.format(command))
    synthServer.run(command)


def sleep(duration):
    """
    the same as time.sleep
    :param duration:
    :return:
    """
    time.sleep(duration)
    _debug('sleep', duration)

## Compount classes ##

class Ring:
    """
    ring buffer
    """
    def __init__(self,data):
        self.data = data
        self.index = -1

    def __iter__(self): #return Iterator
        return self

    def __next__(self): #return Iterator next element
        self.index +=1
        if self.index == len(self.data):
            self.index = 0
        return self.data[self.index]


class Scale(Ring):
    """
    Scale
    """
    def __init__(self,basenote,mode):
        super(Scale,self).__init__([basenote, G3, A3])

    def shuffle(self):
        random.shuffle(self.data)
        return self

## Connection classes ##

class SonicPi():
    """
    Communiction to Sonic Pi
    """

    UDP_IP = "127.0.0.1"
    UDP_PORT = 4557
    GUI_ID = 'SONIC_PI_PYTHON'

    RUN_COMMAND = "/run-code"
    STOP_COMMAND = "/stop-all-jobs"

    def __init__(self):
        self.client = udp_client.UDPClient(SonicPi.UDP_IP, SonicPi.UDP_PORT)

    def run(self, command):
        self.send_command(SonicPi.RUN_COMMAND, command)

    def stop(self):
        self.send_command(SonicPi.STOP_COMMAND)

    def test_connection(self):
        #OSC::Server.new(PORT)
        #abort("ERROR: Sonic Pi is not listening on #{PORT} - is it running?")
        pass

    def send_command(self,address,argument=''):
        msg = osc_message_builder.OscMessageBuilder(address=address)
        msg.add_arg('SONIC_PI_PYTHON')
        msg.add_arg(argument)
        msg = msg.build()

        self.client.send(msg)

synthServer = SonicPi()

## system functions ##

def _debug(*allargs): #simple debug function for working in different environments
    if __debug:print(allargs)


def _init_notes(): #ToDo: __init__
    notes = [["C"],["Cs","Db"],["D"],["Ds","Eb"],["E"],["F"],["Fs","Gb"],["G"],["Gs","As"],["A"],["As","Bb"],["B"]]
    thismodule = sys.modules[__name__]
    setattr(thismodule,'C5',Note('C5',72))

def _init_module(): #ToDo: __init__
    #_init_notes()
    pass

_init_module()
