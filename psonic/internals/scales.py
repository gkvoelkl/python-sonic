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
    'viii': _ionian_sequence[7:] + _ionian_sequence[:7],   # rotate(7)
}


