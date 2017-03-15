#The MIT License (MIT)
#
#Copyright (c) 2016 G. Völkl
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.
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
    def __init__(self, name):
        self.name = name


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
B3 = 47
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
DTRI = Synth('dtri') #Sonic Pi 2.10
PLUCK = Synth('pluck')
CHIPLEAD = Synth('chiplead')
CHIPBASS = Synth('chipbass')
CHIPNOISE = Synth('chipnoise')
TECHSAWS = Synth('tech_saws') #Sonic Pi 2.11
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
    'dorian': _ionian_sequence[1:]+_ionian_sequence[:1], #rotate 1
    'phrygian': _ionian_sequence[2:]+_ionian_sequence[:2], #rotate(2)
    'lydian': _ionian_sequence[3:]+_ionian_sequence[:3], #rotate(3)
    'mixolydian': _ionian_sequence[4:]+_ionian_sequence[:4], #rotate(4)
    'aeolian': _ionian_sequence[5:]+_ionian_sequence[:5], #rotate(5)
    'minor': _ionian_sequence[5:]+_ionian_sequence[:5], #rotate(5)
    'locrian': _ionian_sequence[6:]+_ionian_sequence[:6], #rotate(6)
    'hex_major6': _hex_sequence,
    'hex_dorian': _hex_sequence[1:]+_hex_sequence[:1], #rotate(1)
    'hex_phrygian': _hex_sequence[2:]+_hex_sequence[:2], #rotate(2)
    'hex_major7': _hex_sequence[3:]+_hex_sequence[:3], #rotate(3)
    'hex_sus': _hex_sequence[4:]+_hex_sequence[:4], #rotate(4)
    'hex_aeolian': _hex_sequence[5:]+_hex_sequence[:5], #rotate(5)
    'minor_pentatonic': _pentatonic_sequence,
    'yu': _pentatonic_sequence,
    'major_pentatonic': _pentatonic_sequence[1:]+_pentatonic_sequence[:1], #rotate(1)
    'gong': _pentatonic_sequence[1:]+_pentatonic_sequence[:1], #rotate(1)
    'egyptian': _pentatonic_sequence[2:]+_pentatonic_sequence[:2], #rotate(2)
    'shang': _pentatonic_sequence[2:]+_pentatonic_sequence[:2], #rotate(2)
    'jiao': _pentatonic_sequence[3:]+_pentatonic_sequence[:3], #rotate(3)
    'zhi': _pentatonic_sequence[4:]+_pentatonic_sequence[:4], #rotate(4)
    'ritusen': _pentatonic_sequence[4:]+_pentatonic_sequence[:4], #rotate(4)
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
    'ii': _ionian_sequence[1:]+_ionian_sequence[:1], #rotate(1)
    'iii': _ionian_sequence[2:]+_ionian_sequence[:2], #rotate(2)
    'iv': _ionian_sequence[3:]+_ionian_sequence[:3], #rotate(3)
    'v': _ionian_sequence[4:]+_ionian_sequence[:4], #rotate(4)
    'vi': _ionian_sequence[5:]+_ionian_sequence[:5], #rotate(5)
    'vii': _ionian_sequence[6:]+_ionian_sequence[:6], #rotate(6),
    'viii': _ionian_sequence[7:]+_ionian_sequence[:7]} #rotate(7)

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
DRUM_COWBELL = Sample('drum_cowbell')
DRUM_ROLL = Sample('drum_roll')

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
MISC_CROW = Sample('misc_crow')
MISC_CINEBOOM = Sample('misc_cineboom')

## Percurssive Sounds
PERC_BELL = Sample('perc_bell')
PERC_SWASH = Sample('perc_swash')
PERC_TILL = Sample('perc_till')

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

BD_808 = Sample('bd_808')
BD_ADA = Sample('bd_ada')
BD_BOOM = Sample('bd_boom')
BD_FAT = Sample('bd_fat')
BD_GAS = Sample('bd_gas')
BD_HAUS = Sample('bd_haus')
BD_KLUB = Sample('bd_klub')
BD_PURE = Sample('bd_pure')
BD_SONE = Sample('bd_sone')
BD_TEK = Sample('bd_tek')
BD_ZOME = Sample('bd_zome')
BD_ZUM = Sample('bd_zum')

## Sounds for Looping
LOOP_INDUSTRIAL = Sample('loop_industrial')
LOOP_COMPUS = Sample('loop_compus')
LOOP_AMEN = Sample('loop_amen')
LOOP_AMEN_FULL = Sample('loop_amen_full')
LOOP_SAFARI = Sample('loop_safari')
LOOP_TABLA = Sample('loop_tabla')

## Tabla
TABLA_TAS1 = Sample('tabla_tas1')
TABLA_TAS2 = Sample('tabla_tas2')
TABLA_TAS3 = Sample('tabla_tas3')
TABLA_KE1 = Sample('tabla_ke1')
TABLA_KE2 = Sample('tabla_ke2')
TABLA_KE3 = Sample('tabla_ke3')
TABLA_NA = Sample('tabla_na')
TABLA_NA_O = Sample('tabla_na_o')
TABLA_TUN1 = Sample('tabla_tun1')
TABLA_TUN2 = Sample('tabla_tun2')
TABLA_TUN3 = Sample('tabla_tun3')
TABLA_TE1 = Sample('tabla_te1')
TABLA_TE2 = Sample('tabla_te2')
TABLA_TE_NE = Sample('tabla_te_ne')
TABLA_TE_M = Sample('tabla_te_m')
TABLA_GHE1 = Sample('tabla_ghe1')
TABLA_GHE2 = Sample('tabla_ghe2')
TABLA_GHE3 = Sample('tabla_ghe3')
TABLA_GHE4 = Sample('tabla_ghe4')
TABLA_GHE5 = Sample('tabla_ghe5')
TABLA_GHE6 = Sample('tabla_ghe6')
TABLA_GHE7 = Sample('tabla_ghe7')
TABLA_GHE8 = Sample('tabla_ghe8')
TABLA_DHEC = Sample('tabla_dhec')
TABLA_NA_S = Sample('tabla_na_s')
TABLA_RE = Sample('tabla_re')


# Vinyl
VINYL_BACKSPIN = Sample('vinyl_backspin')
VINYL_REWIND = Sample('vinyl_rewind')
VINYL_SCRATCH = Sample('vinyl_scratch')
VINYL_HISS = Sample('vinyl_hiss')


## Module attributes ##
_current_synth = BEEP


## Module methodes ##
def use_synth(synth):
    global _current_synth
    _current_synth = synth


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

    command = 'use_synth :{0}\n'.format(_current_synth.name) + command
    _debug('play command={}'.format(command))
    synthServer.run(command)


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
            play(i,release=release)
            sleep(t)


def play_pattern(notes):
    """

    :param notes:
    :return:
    """
    play_pattern_timed(notes, 1)


def sample(sample, rate=None, attack=None, sustain=None, release=None,beat_stretch=None,
           start=None, finish=None, amp=None, pan=None):
    parameters = []
    parameter = ''
    command = ''

    if rate is not None: parameters.append('rate: {0}'.format(rate))
    if attack is not None: parameters.append('attack: {0}'.format(attack))
    if sustain is not None: parameters.append('sustain: {0}'.format(sustain))
    if release is not None: parameters.append('release: {0}'.format(release))
    if beat_stretch is not None:parameters.append('beat_stretch: {0}'.format(beat_stretch))
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
        # OSC::Server.new(PORT)
        # abort("ERROR: Sonic Pi is not listening on #{PORT} - is it running?")
        pass

    def send_command(self, address, *args):
        msg = osc_message_builder.OscMessageBuilder(address=address)
        msg.add_arg('SONIC_PI_PYTHON')
        for arg in args:
            msg.add_arg(arg)
        msg = msg.build()

        self.client.send(msg)


synthServer = SonicPi()


## system functions ##

def _debug(*allargs):  # simple debug function for working in different environments
    if __debug: print(allargs)

if __name__ == '__main__':
    use_synth(SAW)
    play(C5, amp=2, pan=-1)
