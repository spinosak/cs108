from sound_base import *

def lowpass(wave, cutoff_hz=800):
    """Apply a butterworth low-pass filter."""
    nyq = SR / 2
    b, a = butter(4, cutoff_hz / nyq, btype='low')
    return lfilter(b, a, wave)

dry      = note(440, 1.5, waveform='sawtooth')
muffled  = lowpass(dry, cutoff_hz=500)
brighter = lowpass(dry, cutoff_hz=3000)

play(dry)
play(muffled)
play(brighter)
save(muffled, "filtered.wav")
