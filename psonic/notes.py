"""Notes"""

root_notes = {
    "C0": 12,
    "Cs0": 13,
    "Db0": 13,
    "D0": 14,
    "Ds0": 15,
    "Eb0": 15,
    "E0": 16,
    "F0": 17,
    "Fs0": 18,
    "Gb0": 18,
    "G0": 19,
    "Gs0": 20,
    "Ab0": 20,
    "A0": 21,
    "As0": 22,
    "Bb0": 22,
    "B0": 23,
}

notes = {}
for octave in range(9):
    for key in root_notes:
        notes[key.replace("0", str(octave))] = root_notes[key] + (12 * octave)

globals().update(notes)

R = 0
