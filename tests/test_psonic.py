from psonic import *

def test_originl_behaviour():
    play(72)
    play(G5)
    sleep(0.5)
    play(72,amp=2)
    play(74,pan=-1)
    use_synth(SAW)
    use_synth(PROPHET)
    play(
        60, attack=0.5, decay=1, sustain_level=0.4,
        sustain=2, release=0.5
    )
    sample(
        LOOP_AMEN, start=0.5, finish=0.8,
        rate=-0.2,attack=0.3,release=1
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
    synth(SQUARE, note = E4+detune)
    synth(GNOISE, release = 0.5, amp = 1, cutoff = 100)



