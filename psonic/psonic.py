# The MIT License (MIT)
#
# Copyright (c) 2016 G. Völkl
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import random
import time
import threading

from pythonosc import osc_message_builder  # osc support
from pythonosc import udp_client

__debug = False


## Base Classes ##

class Synth:
    """
    Synthesizer
    """

    def __init__(self, name):
        self.name = name


class Sample:
    """
    Sample
    """

    def __init__(self, name, duration):
        self.name = name
        self.duration = duration


class ChordQuality:
    """
    Chord Quality
    """

    def __init__(self, name, inter):
        self.name = name
        self.inter = inter


class FxName:
    """
    FX name
    """

    def __init__(self, name):
        self.name = name


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


## Decorator ##

def in_thread(func):
    def wrapper():
        _thread = threading.Thread(target=func)
        _thread.start()

    return wrapper


## Notes ##
C2 = 36
Cs2 = 37
Db2 = Cs2
D2 = 38
Ds2 = 39
Eb2 = Ds2
E2 = 40
F2 = 41
Fs2 = 42
Gb2 = Fs2
G2 = 43
Gs2 = 44
Ab2 = Gs2
A2 = 45
As2 = 46
Bb2 = As2
B2 = 47
C3 = 48
Cs3 = 49
Db3 = Cs3
D3 = 50
Ds3 = 51
Eb3 = Ds3
E3 = 52
F3 = 53
Fs3 = 54
Gb3 = Fs3
G3 = 55
Gs3 = 56
Ab3 = Gs3
A3 = 57
As3 = 58
Bb3 = As3
B3 = 59
C4 = 60
Cs4 = 61
Db4 = Cs4
D4 = 62
Ds4 = 63
Eb4 = Ds4
E4 = 64
F4 = 65
Fs4 = 66
Gb4 = Fs4
G4 = 67
Gs4 = 68
Ab4 = Gs4
A4 = 69
As4 = 70
Bb4 = As4
B4 = 71
C5 = 72
Cs5 = 73
Db5 = Cs5
D5 = 74
Ds5 = 75
Eb5 = Ds5
E5 = 76
F5 = 77
Fs5 = 78
Gb5 = Fs5
G5 = 79
Gs5 = 80
Ab5 = Gs5
A5 = 81
As5 = 82
Bb5 = As5
B5 = 83
C6 = 84

R = 0

## Synthezier ##
DULL_BELL = Synth('dull_bell')
PRETTY_BELL = Synth('pretty_bell')
SINE = Synth('sine')
SQUARE = Synth('square')
PULSE = Synth('pulse')
SUBPULSE = Synth('subpulse')
DTRI = Synth('dtri')
DPULSE = Synth('dpulse')
FM = Synth('fm')
MOD_FM = Synth('mod_fm')
MOD_SAW = Synth('mod_saw')
MOD_DSAW = Synth('mod_dsaw')
MOD_SINE = Synth('mod_sine')
MOD_TRI = Synth('mod_tri')
MOD_PULSE = Synth('mod_pulse')
SUPERSAW = Synth('supersaw')
HOOVER = Synth('hoover')
SYNTH_VIOLIN = Synth('synth_violin')
PLUCK = Synth('pluck')
PIANO = Synth('piano')
GROWL = Synth('growl')
DARK_AMBIENCE = Synth('dark_ambience')
DARK_SEA_HORN = Synth('dark_sea_horn')
HOLLOW = Synth('hollow')
ZAWA = Synth('zawa')
NOISE = Synth('noise')
GNOISE = Synth('gnoise')
BNOISE = Synth('bnoise')
CNOISE = Synth('cnoise')
DSAW = Synth('dsaw')
TB303 = Synth('tb303')
BLADE = Synth('blade')
PROPHET = Synth('prophet')
SAW = Synth('saw')
BEEP = Synth('beep')
TRI = Synth('tri')
CHIPLEAD = Synth('chiplead') # Sonic Pi 2.10
CHIPBASS = Synth('chipbass')
CHIPNOISE = Synth('chipnoise')
TECHSAWS = Synth('tech_saws')  # Sonic Pi 2.11
SOUND_IN = Synth('sound_in')
SOUND_IN_STEREO = Synth('sound_in_stereo')

## Scale Mode (from sonic pi)##
DIATONIC = 'diatonic'
IONIAN = 'ionian'
MAJOR = 'major'
DORIAN = 'dorian'
PHRYGIAN = 'phrygian'
LYDIAN = 'lydian'
MIXOLYDIAN = 'mixolydian'
AEOLIAN = 'aeolian'
MINOR = 'minor'
LOCRIAN = 'locrian'
HEX_MAJOR6 = 'hex_major6'
HEX_DORIAN = 'hex_dorian'
HEX_PHRYGIAN = 'hex_phrygian'
HEX_MAJOR7 = 'hex_major7'
HEX_SUS = 'hex_sus'
HEX_AEOLIAN = 'hex_aeolian'
MINOR_PENTATONIC = 'minor_pentatonic'
YU = 'yu'
MAJOR_PENTATONIC = 'major_pentatonic'
GONG = 'gong'
EGYPTIAN = 'egyptian'
SHANG = 'shang'
JIAO = 'jiao'
ZHI = 'zhi'
RITUSEN = 'ritusen'
WHOLE_TONE = 'whole_tone'
WHOLE = 'whole'
CHROMATIC = 'chromatic'
HARMONIC_MINOR = 'harmonic_minor'
MELODIC_MINOR_ASC = 'melodic_minor_asc'
HUNGARIAN_MINOR = 'hungarian_minor'
OCTATONIC = 'octatonic'
MESSIAEN1 = 'messiaen1'
MESSIAEN2 = 'messiaen2'
MESSIAEN3 = 'messiaen3'
MESSIAEN4 = 'messiaen4'
MESSIAEN5 = 'messiaen5'
MESSIAEN6 = 'messiaen6'
MESSIAEN7 = 'messiaen7'
SUPER_LOCRIAN = 'super_locrian'
HIRAJOSHI = 'hirajoshi'
KUMOI = 'kumoi'
NEAPLOLITAN_MAJOR = 'neapolitan_major'
BARTOK = 'bartok'
BHAIRAV = 'bhairav'
LOCRIAN_MAJOR = 'locrian_major'
AHIRBHAIRAV = 'ahirbhairav'
ENIGMATIC = 'enigmatic'
NEAPLOLITAN_MINOR = 'neapolitan_minor'
PELOG = 'pelog'
AUGMENTED2 = 'augmented2'
SCRIABIN = 'scriabin'
HARMONIC_MAJOR = 'harmonic_major'
MELODIC_MINOR_DESC = 'melodic_minor_desc'
ROMANIAN_MINOR = 'romanian_minor'
HINDU = 'hindu'
IWATO = 'iwato'
MELODIC_MINOR = 'melodic_minor'
DIMISHED2 = 'diminished2'
MARVA = 'marva'
MELODIC_MAJOR = 'melodic_major'
INDIAN = 'indian'
SPANISH = 'spanish'
PROMETHEUS = 'prometheus'
DIMISHED = 'diminished'
TODI = 'todi'
LEADING_WHOLE = 'leading_whole'
AUGMENTED = 'augmented'
PRUVI = 'purvi'
CHINESE = 'chinese'
LYDIAN_MINOR = 'lydian_minor'
I = 'i'
II = 'ii'
III = 'iii'
IV = 'iv'
V = 'v'
VI = 'vi'
VII = 'vii'
VIII = 'viii'
_ionian_sequence = [2, 2, 1, 2, 2, 2, 1]
_hex_sequence = [2, 2, 1, 2, 2, 3]
_pentatonic_sequence = [3, 2, 2, 3, 2]

_SCALE_MODE = {
    'diatonic': _ionian_sequence,
    'ionian': _ionian_sequence,
    'major': _ionian_sequence,
    'dorian': _ionian_sequence[1:] + _ionian_sequence[:1],  # rotate 1
    'phrygian': _ionian_sequence[2:] + _ionian_sequence[:2],  # rotate(2)
    'lydian': _ionian_sequence[3:] + _ionian_sequence[:3],  # rotate(3)
    'mixolydian': _ionian_sequence[4:] + _ionian_sequence[:4],  # rotate(4)
    'aeolian': _ionian_sequence[5:] + _ionian_sequence[:5],  # rotate(5)
    'minor': _ionian_sequence[5:] + _ionian_sequence[:5],  # rotate(5)
    'locrian': _ionian_sequence[6:] + _ionian_sequence[:6],  # rotate(6)
    'hex_major6': _hex_sequence,
    'hex_dorian': _hex_sequence[1:] + _hex_sequence[:1],  # rotate(1)
    'hex_phrygian': _hex_sequence[2:] + _hex_sequence[:2],  # rotate(2)
    'hex_major7': _hex_sequence[3:] + _hex_sequence[:3],  # rotate(3)
    'hex_sus': _hex_sequence[4:] + _hex_sequence[:4],  # rotate(4)
    'hex_aeolian': _hex_sequence[5:] + _hex_sequence[:5],  # rotate(5)
    'minor_pentatonic': _pentatonic_sequence,
    'yu': _pentatonic_sequence,
    'major_pentatonic': _pentatonic_sequence[1:] + _pentatonic_sequence[:1],  # rotate(1)
    'gong': _pentatonic_sequence[1:] + _pentatonic_sequence[:1],  # rotate(1)
    'egyptian': _pentatonic_sequence[2:] + _pentatonic_sequence[:2],  # rotate(2)
    'shang': _pentatonic_sequence[2:] + _pentatonic_sequence[:2],  # rotate(2)
    'jiao': _pentatonic_sequence[3:] + _pentatonic_sequence[:3],  # rotate(3)
    'zhi': _pentatonic_sequence[4:] + _pentatonic_sequence[:4],  # rotate(4)
    'ritusen': _pentatonic_sequence[4:] + _pentatonic_sequence[:4],  # rotate(4)
    'whole_tone': [2, 2, 2, 2, 2, 2],
    'whole': [2, 2, 2, 2, 2, 2],
    'chromatic': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    'harmonic_minor': [2, 1, 2, 2, 1, 3, 1],
    'melodic_minor_asc': [2, 1, 2, 2, 2, 2, 1],
    'hungarian_minor': [2, 1, 3, 1, 1, 3, 1],
    'octatonic': [2, 1, 2, 1, 2, 1, 2, 1],
    'messiaen1': [2, 2, 2, 2, 2, 2],
    'messiaen2': [1, 2, 1, 2, 1, 2, 1, 2],
    'messiaen3': [2, 1, 1, 2, 1, 1, 2, 1, 1],
    'messiaen4': [1, 1, 3, 1, 1, 1, 3, 1],
    'messiaen5': [1, 4, 1, 1, 4, 1],
    'messiaen6': [2, 2, 1, 1, 2, 2, 1, 1],
    'messiaen7': [1, 1, 1, 2, 1, 1, 1, 1, 2, 1],
    'super_locrian': [1, 2, 1, 2, 2, 2, 2],
    'hirajoshi': [2, 1, 4, 1, 4],
    'kumoi': [2, 1, 4, 2, 3],
    'neapolitan_major': [1, 2, 2, 2, 2, 2, 1],
    'bartok': [2, 2, 1, 2, 1, 2, 2],
    'bhairav': [1, 3, 1, 2, 1, 3, 1],
    'locrian_major': [2, 2, 1, 1, 2, 2, 2],
    'ahirbhairav': [1, 3, 1, 2, 2, 1, 2],
    'enigmatic': [1, 3, 2, 2, 2, 1, 1],
    'neapolitan_minor': [1, 2, 2, 2, 1, 3, 1],
    'pelog': [1, 2, 4, 1, 4],
    'augmented2': [1, 3, 1, 3, 1, 3],
    'scriabin': [1, 3, 3, 2, 3],
    'harmonic_major': [2, 2, 1, 2, 1, 3, 1],
    'melodic_minor_desc': [2, 1, 2, 2, 1, 2, 2],
    'romanian_minor': [2, 1, 3, 1, 2, 1, 2],
    'hindu': [2, 2, 1, 2, 1, 2, 2],
    'iwato': [1, 4, 1, 4, 2],
    'melodic_minor': [2, 1, 2, 2, 2, 2, 1],
    'diminished2': [2, 1, 2, 1, 2, 1, 2, 1],
    'marva': [1, 3, 2, 1, 2, 2, 1],
    'melodic_major': [2, 2, 1, 2, 1, 2, 2],
    'indian': [4, 1, 2, 3, 2],
    'spanish': [1, 3, 1, 2, 1, 2, 2],
    'prometheus': [2, 2, 2, 5, 1],
    'diminished': [1, 2, 1, 2, 1, 2, 1, 2],
    'todi': [1, 2, 3, 1, 1, 3, 1],
    'leading_whole': [2, 2, 2, 2, 2, 1, 1],
    'augmented': [3, 1, 3, 1, 3, 1],
    'purvi': [1, 3, 2, 1, 1, 3, 1],
    'chinese': [4, 2, 1, 4, 1],
    'lydian_minor': [2, 2, 2, 1, 1, 2, 2],
    'i': _ionian_sequence,
    'ii': _ionian_sequence[1:] + _ionian_sequence[:1],  # rotate(1)
    'iii': _ionian_sequence[2:] + _ionian_sequence[:2],  # rotate(2)
    'iv': _ionian_sequence[3:] + _ionian_sequence[:3],  # rotate(3)
    'v': _ionian_sequence[4:] + _ionian_sequence[:4],  # rotate(4)
    'vi': _ionian_sequence[5:] + _ionian_sequence[:5],  # rotate(5)
    'vii': _ionian_sequence[6:] + _ionian_sequence[:6],  # rotate(6),
    'viii': _ionian_sequence[7:] + _ionian_sequence[:7]}  # rotate(7)

## Chord Quality (from sonic pi) ##
MAJOR7 = "major7"
DOM7 = "dom7"
MINOR7 = "minor7"
AUG = "aug"
DIM = "dim"
DIM7 = "dim7"

_CHORD_QUALITY = {
    'major': [0, 4, 7],
    'minor': [0, 3, 7],
    'major7': [0, 4, 7, 11],
    'dom7': [0, 4, 7, 10],
    'minor7': [0, 3, 7, 10],
    'aug': [0, 4, 8],
    'dim': [0, 3, 6],
    'dim7': [0, 3, 6, 9],
    '1': [0],
    "5": [0, 7],
    "+5": [0, 4, 8],
    "m+5": [0, 3, 8],
    "sus2": [0, 2, 7],
    "sus4": [0, 5, 7],
    "6": [0, 4, 7, 9],
    "m6": [0, 3, 7, 9],
    "7sus2": [0, 2, 7, 10],
    "7sus4": [0, 5, 7, 10],
    "7-5": [0, 4, 6, 10],
    "m7-5": [0, 3, 6, 10],
    "7+5": [0, 4, 8, 10],
    "m7+5": [0, 3, 8, 10],
    "9": [0, 4, 7, 10, 14],
    "m9": [0, 3, 7, 10, 14],
    "m7+9": [0, 3, 7, 10, 14],
    "maj9": [0, 4, 7, 11, 14],
    "9sus4": [0, 5, 7, 10, 14],
    "6*9": [0, 4, 7, 9, 14],
    "m6*9": [0, 3, 9, 7, 14],
    "7-9": [0, 4, 7, 10, 13],
    "m7-9": [0, 3, 7, 10, 13],
    "7-10": [0, 4, 7, 10, 15],
    "9+5": [0, 10, 13],
    "m9+5": [0, 10, 14],
    "7+5-9": [0, 4, 8, 10, 13],
    "m7+5-9": [0, 3, 8, 10, 13],
    "11": [0, 4, 7, 10, 14, 17],
    "m11": [0, 3, 7, 10, 14, 17],
    "maj11": [0, 4, 7, 11, 14, 17],
    "11+": [0, 4, 7, 10, 14, 18],
    "m11+": [0, 3, 7, 10, 14, 18],
    "13": [0, 4, 7, 10, 14, 17, 21],
    "m13": [0, 3, 7, 10, 14, 17, 21],
    "M": [0, 4, 7],
    "m": [0, 3, 7],
    "7": [0, 4, 7, 10],
    "M7": [0, 4, 7, 11],
    "m7": [0, 3, 7],
    "augmented": [0, 4, 8],
    "a": [0, 4, 8],
    "diminished": [0, 3, 6],
    "i": [0, 3, 6],
    "diminished7": [0, 3, 6, 9],
    "i7": [0, 3, 6, 9]}

## Sample ##

## Drum Sounds
DRUM_BASS_HARD = Sample('drum_bass_hard', 0.6951927437641723)
DRUM_BASS_SOFT = Sample('drum_bass_soft', 0.5624489795918367)
DRUM_COWBELL = Sample('drum_cowbell', 0.34988662131519277)
DRUM_CYMBAL_CLOSED = Sample('drum_cymbal_closed', 0.2069387755102041)
DRUM_CYMBAL_HARD = Sample('drum_cymbal_hard', 1.6388208616780044)
DRUM_CYMBAL_OPEN = Sample('drum_cymbal_open', 1.8043764172335601)
DRUM_CYMBAL_PEDAL = Sample('drum_cymbal_pedal', 0.2721995464852608)
DRUM_CYMBAL_SOFT = Sample('drum_cymbal_soft', 0.9497278911564626)
DRUM_HEAVY_KICK = Sample('drum_heavy_kick', 0.2701360544217687)
DRUM_ROLL = Sample('drum_roll', 6.241678004535148)
DRUM_SNARE_HARD = Sample('drum_snare_hard', 0.44492063492063494)
DRUM_SNARE_SOFT = Sample('drum_snare_soft', 0.3147845804988662)
DRUM_SPLASH_HARD = Sample('drum_splash_hard', 2.5961904761904764)
DRUM_SPLASH_SOFT = Sample('drum_splash_soft', 1.857981859410431)
DRUM_TOM_HI_HARD = Sample('drum_tom_hi_hard', 0.7376643990929705)
DRUM_TOM_HI_SOFT = Sample('drum_tom_hi_soft', 0.6290249433106576)
DRUM_TOM_LO_HARD = Sample('drum_tom_lo_hard', 1.0002267573696144)
DRUM_TOM_LO_SOFT = Sample('drum_tom_lo_soft', 0.8634013605442177)
DRUM_TOM_MID_HARD = Sample('drum_tom_mid_hard', 0.7342176870748299)
DRUM_TOM_MID_SOFT = Sample('drum_tom_mid_soft', 0.6721315192743764)

## Electric Sounds
ELEC_BEEP = Sample('elec_beep', 0.10578231292517007)
ELEC_BELL = Sample('elec_bell', 0.27825396825396825)
ELEC_BLIP = Sample('elec_blip', 0.15816326530612246)
ELEC_BLIP2 = Sample('elec_blip2', 0.1840816326530612)
ELEC_BLUP = Sample('elec_blup', 0.6632199546485261)
ELEC_BONG = Sample('elec_bong', 0.3464852607709751)
ELEC_CHIME = Sample('elec_chime', 2.2775510204081635)
ELEC_CYMBAL = Sample('elec_cymbal', 0.563219954648526)
ELEC_FILT_SNARE = Sample('elec_filt_snare', 1.5158503401360544)
ELEC_FLIP = Sample('elec_flip', 0.07476190476190477)
ELEC_FUZZ_TOM = Sample('elec_fuzz_tom', 0.37179138321995464)
ELEC_HI_SNARE = Sample('elec_hi_snare', 0.19736961451247165)
ELEC_HOLLOW_KICK = Sample('elec_hollow_kick', 0.15564625850340136)
ELEC_LO_SNARE = Sample('elec_lo_snare', 0.6607936507936508)
ELEC_MID_SNARE = Sample('elec_mid_snare', 0.7256235827664399)
ELEC_PING = Sample('elec_ping', 0.21226757369614513)
ELEC_PLIP = Sample('elec_plip', 0.19882086167800453)
ELEC_POP = Sample('elec_pop', 0.08680272108843537)
ELEC_SNARE = Sample('elec_snare', 0.3893197278911565)
ELEC_SOFT_KICK = Sample('elec_soft_kick', 0.1364172335600907)
ELEC_TICK = Sample('elec_tick', 0.01943310657596372)
ELEC_TRIANGLE = Sample('elec_triangle', 0.22294784580498866)
ELEC_TWANG = Sample('elec_twang', 0.6243083900226757)
ELEC_TWIP = Sample('elec_twip', 0.10140589569160997)
ELEC_WOOD = Sample('elec_wood', 0.47811791383219954)

## Sounds featuring guitars
GUIT_E_FIFTHS = Sample('guit_e_fifths', 5.971791383219955)
GUIT_E_SLIDE = Sample('guit_e_slide', 4.325192743764172)
GUIT_EM9 = Sample('guit_em9', 9.972063492063493)
GUIT_HARMONICS = Sample('guit_harmonics', 3.5322675736961453)

## Miscellaneous Sounds
MISC_BURP = Sample('misc_burp', 0.7932879818594104)
MISC_CINEBOOM = Sample('misc_cineboom', 7.922675736961451)
MISC_CROW = Sample('misc_crow', 0.48063492063492064)

## Percurssive Sounds
PERC_BELL = Sample('perc_bell', 6.719206349206349)
PERC_SNAP = Sample('perc_snap', 0.30795918367346936)
PERC_SNAP2 = Sample('perc_snap2', 0.17414965986394557)
PERC_SWASH = Sample('perc_swash', 0.3195011337868481)
PERC_TILL = Sample('perc_till', 2.665736961451247)

## Ambient Sounds
AMBI_CHOIR = Sample('ambi_choir', 1.5715419501133787)
AMBI_DARK_WOOSH = Sample('ambi_dark_woosh', 3.7021315192743764)
AMBI_DRONE = Sample('ambi_drone', 4.40843537414966)
AMBI_GLASS_HUM = Sample('ambi_glass_hum', 10.0)
AMBI_GLASS_RUB = Sample('ambi_glass_rub', 3.1493650793650794)
AMBI_HAUNTED_HUM = Sample('ambi_haunted_hum', 9.78156462585034)
AMBI_LUNAR_LAND = Sample('ambi_lunar_land', 7.394240362811791)
AMBI_PIANO = Sample('ambi_piano', 2.811746031746032)
AMBI_SOFT_BUZZ = Sample('ambi_soft_buzz', 0.7821541950113379)
AMBI_SWOOSH = Sample('ambi_swoosh', 1.8484580498866212)

## Bass Sounds
BASS_DNB_F = Sample('bass_dnb_f', 0.8705442176870748)
BASS_DROP_C = Sample('bass_drop_c', 2.3589115646258505)
BASS_HARD_C = Sample('bass_hard_c', 1.5)
BASS_HIT_C = Sample('bass_hit_c', 0.6092517006802721)
BASS_THICK_C = Sample('bass_thick_c', 3.9680725623582767)
BASS_VOXY_C = Sample('bass_voxy_c', 6.23469387755102)
BASS_VOXY_HIT_C = Sample('bass_voxy_hit_c', 0.457437641723356)
BASS_WOODSY_C = Sample('bass_woodsy_c', 3.252267573696145)

## Snare Drums Sounds
SN_DOLF = Sample('sn_dolf', 0.37759637188208617)
SN_DUB = Sample('sn_dub', 0.2781179138321995)
SN_ZOME = Sample('sn_zome', 0.4787528344671202)

## Bass Drums Sounds
BD_808 = Sample('bd_808', 0.5597505668934241)
BD_ADA = Sample('bd_ada', 0.10179138321995465)
BD_BOOM = Sample('bd_boom', 1.7142857142857142)
BD_FAT = Sample('bd_fat', 0.23219954648526078)
BD_GAS = Sample('bd_gas', 0.4471428571428571)
BD_HAUS = Sample('bd_haus', 0.21993197278911564)
BD_KLUB = Sample('bd_klub', 0.368843537414966)
BD_PURE = Sample('bd_pure', 0.43324263038548755)
BD_SONE = Sample('bd_sone', 0.4089115646258503)
BD_TEK = Sample('bd_tek', 0.24024943310657595)
BD_ZOME = Sample('bd_zome', 0.45972789115646256)
BD_ZUM = Sample('bd_zum', 0.13158730158730159)

## Sounds for Looping
LOOP_AMEN = Sample('loop_amen', 1.753310657596372)
LOOP_AMEN_FULL = Sample('loop_amen_full', 6.857142857142857)
LOOP_BREAKBEAT = Sample('loop_breakbeat', 1.9047619047619047)
LOOP_COMPUS = Sample('loop_compus', 6.486485260770975)
LOOP_GARZUL = Sample('loop_garzul', 8.0)
LOOP_INDUSTRIAL = Sample('loop_industrial', 0.8837414965986394)
LOOP_MIKA = Sample('loop_mika', 8.0)
LOOP_SAFARI = Sample('loop_safari', 8.005079365079364)
LOOP_TABLA = Sample('loop_tabla', 10.673990929705216)

## Tabla
TABLA_DHEC = Sample('tabla_dhec', 0.3250793650793651)
TABLA_GHE1 = Sample('tabla_ghe1', 0.5912244897959184)
TABLA_GHE2 = Sample('tabla_ghe2', 2.6607256235827665)
TABLA_GHE3 = Sample('tabla_ghe3', 2.3908163265306124)
TABLA_GHE4 = Sample('tabla_ghe4', 0.7960997732426304)
TABLA_GHE5 = Sample('tabla_ghe5', 3.560045351473923)
TABLA_GHE6 = Sample('tabla_ghe6', 3.6011337868480724)
TABLA_GHE7 = Sample('tabla_ghe7', 2.1512698412698414)
TABLA_GHE8 = Sample('tabla_ghe8', 0.5817913832199546)
TABLA_KE1 = Sample('tabla_ke1', 0.04342403628117914)
TABLA_KE2 = Sample('tabla_ke2', 0.04403628117913832)
TABLA_KE3 = Sample('tabla_ke3', 0.07571428571428572)
TABLA_NA = Sample('tabla_na', 0.7198185941043084)
TABLA_NA_O = Sample('tabla_na_o', 1.4889795918367348)
TABLA_NA_S = Sample('tabla_na_s', 0.23582766439909297)
TABLA_RE = Sample('tabla_re', 0.2815419501133787)
TABLA_TAS1 = Sample('tabla_tas1', 1.1116553287981858)
TABLA_TAS2 = Sample('tabla_tas2', 1.4338321995464853)
TABLA_TAS3 = Sample('tabla_tas3', 1.2364625850340136)
TABLA_TE1 = Sample('tabla_te1', 0.17777777777777778)
TABLA_TE2 = Sample('tabla_te2', 0.33233560090702946)
TABLA_TE_M = Sample('tabla_te_m', 0.28879818594104306)
TABLA_TE_NE = Sample('tabla_te_ne', 0.15310657596371882)
TABLA_TUN1 = Sample('tabla_tun1', 2.3394104308390022)
TABLA_TUN2 = Sample('tabla_tun2', 2.693514739229025)
TABLA_TUN3 = Sample('tabla_tun3', 2.0956009070294783)

# Vinyl
VINYL_BACKSPIN = Sample('vinyl_backspin', 1.06124716553288)
VINYL_HISS = Sample('vinyl_hiss', 8.0)
VINYL_REWIND = Sample('vinyl_rewind', 2.6804761904761905)
VINYL_SCRATCH = Sample('vinyl_scratch', 0.27383219954648524)

## FX
BITCRUSHER = FxName('bitcrusher')
COMPRESSOR = FxName('compressor')
ECHO = FxName('echo')
FLANGER = FxName('flanger')
KRUSH = FxName('krush')
LPF = FxName('lpf')
PAN = FxName('pan')
PANSLICER = FxName('panslicer')
REVERB = FxName('reverb')
SLICER = FxName('slicer')
WOBBLE = FxName('wobble')

## Module attributes ##
_current_synth = BEEP


## Module methodes ##
def use_synth(synth):
    global _current_synth
    _current_synth = synth


def synth(name, note=None, attack=None, decay=None, sustain_level=None, sustain=None, release=None, cutoff=None,
          cutoff_attack=None, amp=None, pan=None):
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
