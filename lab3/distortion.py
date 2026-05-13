from sound_base import *

def distort(wave, gain=10.0, clip=0.3):
    """Amplify then hard-clip."""
    driven = wave * gain
    return np.clip(driven, -clip, clip) * (0.8 / clip)

dry        = note(220, 1.5, amplitude=0.3, waveform='sine')
mild_dist  = distort(dry, gain=3,  clip=0.5)
heavy_dist = distort(dry, gain=20, clip=0.1)

show(dry,        "clean",         duration=0.01)
show(mild_dist,  "mild distortion", duration=0.01)
show(heavy_dist, "heavy distortion", duration=0.01)

play(dry)
play(mild_dist)
play(heavy_dist)