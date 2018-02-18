from . import Sample

## Bass Sounds
BASS_DNB_F = Sample('bass_dnb_f', 0.8705442176870748)
BASS_DROP_C = Sample('bass_drop_c', 2.3589115646258505)
BASS_HARD_C = Sample('bass_hard_c', 1.5)
BASS_HIT_C = Sample('bass_hit_c', 0.6092517006802721)
BASS_THICK_C = Sample('bass_thick_c', 3.9680725623582767)
BASS_VOXY_C = Sample('bass_voxy_c', 6.23469387755102)
BASS_VOXY_HIT_C = Sample('bass_voxy_hit_c', 0.457437641723356)
BASS_WOODSY_C = Sample('bass_woodsy_c', 3.252267573696145)


def get_sounds():
    sounds = dict(
        BASS_DNB_F = BASS_DNB_F,
        BASS_DROP_C = BASS_DROP_C,
        BASS_HARD_C = BASS_HARD_C,
        BASS_HIT_C = BASS_HIT_C,
        BASS_THICK_C = BASS_THICK_C,
        BASS_VOXY_C = BASS_VOXY_C,
        BASS_VOXY_HIT_C = BASS_VOXY_HIT_C,
        BASS_WOODSY_C = BASS_WOODSY_C,
    )
    return sounds
