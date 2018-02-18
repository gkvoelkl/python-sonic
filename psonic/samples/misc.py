from . import Sample
## Miscellaneous Sounds
MISC_BURP = Sample('misc_burp', 0.7932879818594104)
MISC_CINEBOOM = Sample('misc_cineboom', 7.922675736961451)
MISC_CROW = Sample('misc_crow', 0.48063492063492064)

def get_sounds():

    sounds = dict(
        MISC_BURP = MISC_BURP,
        MISC_CINEBOOM = MISC_CINEBOOM,
        MISC_CROW = MISC_CROW,
    )
    return sounds

