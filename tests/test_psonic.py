import pytest
from psonic import *

def test_originl_behaviour():
    notes_to_play = [72, G5, Fs5, Eb5]
    (play(note) for note in notes_to_play)
    sleep(0.5)
    play(72, amp=2)
    play(74, pan=-1)
    use_synth(SAW)
    use_synth(PROPHET)
    play(
        60, attack=0.5, decay=1, sustain_level=0.4,
        sustain=2, release=0.5
    )
    sample(
        LOOP_AMEN, start=0.5, finish=0.8,
        rate=-0.2, attack=0.3, release=1
    )
    sample(
        DRUM_CYMBAL_OPEN, attack=0.01,
        sustain=0.3, release=0.1
    )
    play([64, 67, 71], amp = 0.3)
    play(chord(E4, MINOR7))
    play_pattern_timed(
        scale(
            C3, MAJOR_PENTATONIC, num_octaves = 2
        ),
        0.125, release = 0.1,
    )
    synth(TRI, note=D4, amp=0.4)
    detune = 0.7
    synth(SQUARE, note=E4+detune)
    synth(GNOISE, release=0.5, amp=1, cutoff=100)
    sc = Ring(scale(E3, MINOR_PENTATONIC))
    play(next(sc), release=0.1)
    with Fx(SLICER):
        synth(PROPHET, note=E2, release=8, cutoff=80)
        synth(PROPHET, note=E2+4, release=8, cutoff=80)
    run("""live_loop :foo do
        use_real_time
        a, b, c = sync "/osc/trigger/prophet"
        synth :prophet, note: a, cutoff: b, sustain: c
        end """)
    send_message('/trigger/prophet', 70, 100, 8)
    stop()


@pytest.mark.parametrize("root,quality,inversion,result", (
    (C4, MAJOR, None, [C4, E4, G4]),
    (C4, MAJOR, 0, [C4, E4, G4]),
    (C4, MAJOR, 1, [G3, C4, E4]),
    (C4, MAJOR, 2, [E3, G3, C4]),
    (C4, MAJOR, 3, [C4, E4, G4]),
    (C4, MAJOR, 4, [G3, C4, E4]),
    (C4, MAJOR7, 0, [C4, E4, G4, B4]),
    (C4, MAJOR7, 1, [B3, C4, E4, G4]),
    (C4, MAJOR7, 2, [G3, B3, C4, E4]),
    (C4, MAJOR7, 3, [E3, G3, B3, C4]),
    (C4, MAJOR7, 4, [C4, E4, G4, B4]),
    (C4, MAJOR7, 5, [B3, C4, E4, G4]),
))
def test_chord_inversions(root, quality, inversion, result):
    assert chord(root, quality, inversion) == result


def test_imports():
    from psonic import(
        SonicPi,
        SonicPiNew,
        ChordQuality,
        Message,
        Ring,
        Fx,
        Synth,
        Sample,
    )
