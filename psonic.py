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
    all = {}

    def __init__(self,name,midi):
        self.name = name
        self.midi = midi

        if not self.midi in Note.all : Note.all[self.midi] = self

    def __add__(self, other):
        return Note.all[self.midi + other]

class Synth:
    """
    Synthesizer
    """
    def __init__(self,name):
        self.name = name


class Sample:
    """
    Sample
    """
    def __init__(self,name):
        self.name = name


class ChordQuality:
    """
    Chord Quality
    """
    def __init__(self,name,inter):
        self.name = name
        self.inter = inter


## Notes ##
C3 = Note('C3',48)
Cs3 = Note('Cs3',49)
Db3 = Cs3
D3 = Note('D3',50)
Ds3 = Note('Ds3',51)
Eb3 = Ds3
E3 = Note('E3',52)
F3 = Note('F3',53)
Fs3 = Note('Fs3',54)
Gb3 = Fs3
G3 = Note('G3',55)
Gs3 = Note('Gs3',56)
Ab3 = Gs3
A3 = Note('A3',57)
As3 = Note('As3',58)
Bb3 = As3
B3 = Note('B3',59)
C4 = Note('C4',60)
Cs4 = Note('Cs4',61)
Db4 = Cs4
D4 = Note('D4',62)
Ds4 = Note('Ds4',63)
Eb4 = Ds4
E4 = Note('E4',64)
F4 = Note('F4',65)
Fs4 = Note('Fs4',66)
Gb4 = Fs4
G4 = Note('G4',67)
Gs4 = Note('Gs4',68)
Ab4 = Gs4
A4 = Note('A4',69)
As4 = Note('As4',70)
Bb4 = As4
B4 = Note('B4',71)
C5 = Note('C5',72)
Cs5 = Note('Cs5',73)
Db5 = Cs5
D5 = Note('D5',74)
Ds5 = Note('Ds5',75)
Eb5 = Ds5
E5 = Note('E5',76)
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

## Chord Quality ##
M7 = ChordQuality('m7',[3,4,3])

## Sample ##

## Drum Sounds
DRUM_HEAVY_KICK = Sample('drum_heavy_kick')
DRUM_TOM_MID_SOFT = Sample('drum_tom_mid_soft')
DRUM_TOM_MID_HARD = Sample('drum_tom_mid_hard')
DRUM_TOM_LO_SOFT = Sample('drum_tom_lo_soft')
DRUM_TOM_LO_HARD = Sample('drum_tom_lo_hard')
DRUM_TOM_HI_SOFT = Sample('drum_tom_hi_soft')
DRUM_TOM_HI_HARD = Sample('drum_tom_hi_hard')
DRUM_SPLASH_SOFT = Sample('drum_splash_soft')
DRUM_SPLASH_HARD = Sample('drum_splash_hard')
DRUM_SNARE_SOFT = Sample('drum_snare_soft')
DRUM_SNARE_HARD = Sample('drum_snare_hard')
DRUM_CYMBAL_SOFT = Sample('drum_cymbal_soft')
DRUM_CYMBAL_HARD = Sample('drum_cymbal_hard')
DRUM_CYMBAL_OPEN = Sample('drum_cymbal_open')
DRUM_CYMBAL_CLOSED = Sample('drum_cymbal_closed')
DRUM_CYMBAL_PEDAL = Sample('drum_cymbal_pedal')
DRUM_BASS_SOFT = Sample('drum_bass_soft')
DRUM_BASS_HARD = Sample('drum_bass_hard')

## Electric Sounds
ELEC_TRIANGLE = Sample('elec_triangle')
ELEC_SNARE = Sample('elec_snare')
ELEC_LO_SNARE = Sample('elec_lo_snare')
ELEC_HI_SNARE = Sample('elec_hi_snare')
ELEC_MID_SNARE = Sample('elec_mid_snare')
ELEC_CYMBAL = Sample('elec_cymbal')
ELEC_SOFT_KICK = Sample('elec_soft_kick')
ELEC_FILT_SNARE = Sample('elec_filt_snare')
ELEC_FUZZ_TOM = Sample('elec_fuzz_tom')
ELEC_CHIME = Sample('elec_chime')
ELEC_BONG = Sample('elec_bong')
ELEC_TWANG = Sample('elec_twang')
ELEC_WOOD = Sample('elec_wood')
ELEC_POP = Sample('elec_pop')
ELEC_BEEP = Sample('elec_beep')
ELEC_BLIP = Sample('elec_blip')
ELEC_BLIP2 = Sample('elec_blip2')
ELEC_PING = Sample('elec_ping')
ELEC_BELL = Sample('elec_bell')
ELEC_FLIP = Sample('elec_flip')
ELEC_TICK = Sample('elec_tick')
ELEC_HOLLOW_KICK = Sample('elec_hollow_kick')
ELEC_TWIP = Sample('elec_twip')
ELEC_PLIP = Sample('elec_plip')
ELEC_BLUP = Sample('elec_blup')

## Sounds featuring guitars
GUIT_HARMONICS = Sample('guit_harmonics')
GUIT_E_FIFTHS = Sample('guit_e_fifths')
GUIT_E_SLIDE = Sample('guit_e_slide')

## Miscellaneous Sounds
MISC_BURP = Sample('misc_burp')

## Percurssive Sounds
PERC_BELL = Sample('perc_bell')


## Ambient Sounds
AMBI_SOFT_BUZZ = Sample('ambi_soft_buzz')
AMBI_SWOOSH = Sample('ambi_swoosh')
AMBI_DRONE = Sample('ambi_drone')
AMBI_GLASS_HUM = Sample('ambi_glass_hum')
AMBI_GLASS_RUB = Sample('ambi_glass_rub')
AMBI_HAUNTED_HUM = Sample('ambi_haunted_hum')
AMBI_PIANO = Sample('ambi_piano')
AMBI_LUNAR_LAND = Sample('ambi_lunar_land')
AMBI_DARK_WOOSH = Sample('ambi_dark_woosh')
AMBI_CHOIR = Sample('ambi_choir')

## Bass Sounds
BASS_HIT_C = Sample('bass_hit_c')
BASS_HARD_C = Sample('bass_hard_c')
BASS_THICK_C = Sample('bass_thick_c')
BASS_DROP_C = Sample('bass_drop_c')
BASS_WOODSY_C = Sample('bass_woodsy_c')
BASS_VOXY_C = Sample('bass_voxy_c')
BASS_VOXY_HIT_C = Sample('bass_voxy_hit_c')
BASS_DNB_F = Sample('bass_dnb_f')

## Sounds for Looping
LOOP_INDUSTRIAL = Sample('loop_industrial')
LOOP_COMPUS = Sample('loop_compus')
LOOP_AMEN = Sample('loop_amen')
LOOP_AMEN_FULL = Sample('loop_amen_full')


## Module attributes ##
_current_synth = BEEP

## Module methodes ##
def use_synth(synth):
    global _current_synth
    _current_synth = synth


def play(note, attack=None, decay=None, sustain_level=None, sustain=None, release=None, cutoff=None, amp=None, pan=None):
    parameters = []
    parameter = ''
    command = ''

    if attack is not None: parameters.append('attack: {0}'.format(attack))
    if decay  is not None: parameters.append('decay: {0}'.format(decay))
    if sustain_level is not None: parameters.append('sustain_level: {0}'.format(sustain_level))
    if sustain is not None: parameters.append('sustain: {0}'.format(sustain))
    if release is not None: parameters.append('release: {0}'.format(release))
    if cutoff is not None: parameters.append('cutoff: {0}'.format(cutoff))

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


def sample(sample, rate=None,attack=None,sustain=None,release=None,start=None,finish=None, amp=None, pan=None):
    parameters = []
    parameter = ''
    command = ''

    if rate is not None: parameters.append('rate: {0}'.format(rate))
    if attack is not None: parameters.append('attack: {0}'.format(attack))
    if sustain is not None: parameters.append('sustain: {0}'.format(sustain))
    if release is not None: parameters.append('release: {0}'.format(release))
    if start is not None: parameters.append('start: {0}'.format(start))
    if finish is not None: parameters.append('finish: {0}'.format(finish))
    if amp is not None: parameters.append('amp: {0}'.format(amp))
    if pan is not None: parameters.append('pan: {0}'.format(pan))

    if len(parameters)>0: parameter = ',' + ','.join(parameters)

    if type(sample) == Sample :
        command = 'sample :{0}{1}'.format(sample.name,parameter)
    else:
        command = 'sample "{0}"{1}'.format(sample,parameter)

    _debug('sample command={}'.format(command))
    synthServer.run(command)


def sleep(duration):
    """
    the same as time.sleep
    :param duration:
    :return:
    """
    time.sleep(duration)
    _debug('sleep', duration)

def one_in(max):
    """
    random function  returns True in one of max cases
    :param max:
    :return: boolean
    """
    return random.randint(1,max) == 1

## Compound classes ##

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

    def choose(self): #random choose
        return random.choice(self.data)

class Scale(Ring):
    """
    Scale
    """
    def __init__(self,basenote,mode):
        super(Scale,self).__init__([basenote, G3, A3])

    def shuffle(self):
        random.shuffle(self.data)
        return self


class Chord(Ring):
    """
    Chord
    """
    def __init__(self,root_note,chord_quality):
        notes = [root_note]
        n = root_note
        for i in chord_quality.inter:
            n = n + i
            notes.append(n)
        super(Chord,self).__init__(notes)

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
