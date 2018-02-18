from . import Sample
## Percurssive Sounds
PERC_BELL = Sample('perc_bell', 6.719206349206349)
PERC_SNAP = Sample('perc_snap', 0.30795918367346936)
PERC_SNAP2 = Sample('perc_snap2', 0.17414965986394557)
PERC_SWASH = Sample('perc_swash', 0.3195011337868481)
PERC_TILL = Sample('perc_till', 2.665736961451247)


def get_sounds():

    sounds = dict(
        PERC_BELL = PERC_BELL,
        PERC_SNAP = PERC_SNAP,
        PERC_SNAP2 = PERC_SNAP2,
        PERC_SWASH = PERC_SWASH,
        PERC_TILL = PERC_TILL,
    )
    return sounds
