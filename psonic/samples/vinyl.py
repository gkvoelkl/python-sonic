from . import Sample
# Vinyl
VINYL_BACKSPIN = Sample('vinyl_backspin', 1.06124716553288)
VINYL_HISS = Sample('vinyl_hiss', 8.0)
VINYL_REWIND = Sample('vinyl_rewind', 2.6804761904761905)
VINYL_SCRATCH = Sample('vinyl_scratch', 0.27383219954648524)

def get_sounds():

    sounds = dict(
        VINYL_BACKSPIN = VINYL_BACKSPIN,
        VINYL_HISS = VINYL_HISS,
        VINYL_REWIND = VINYL_REWIND,
        VINYL_SCRATCH = VINYL_SCRATCH,
    )
    return sounds
