from sound_base import *

def note(freq, duration, amplitude=0.3, waveform='sine'):
    t = timeline(duration)
    if waveform == 'sine':
        wave = np.sin(2 * np.pi * freq * t)
    elif waveform == 'sawtooth':
        wave = 2 * (t * freq % 1) - 1
    elif waveform == 'square':
        wave = np.sign(np.sin(2 * np.pi * freq * t))

    env = adsr(duration, attack=0.02, decay=0.1, sustain=0.6, release=0.15)
    return amplitude * wave * env

def semitones(base_freq, steps):
    """Shift a frequency by `steps` semitones."""
    return base_freq * (2 ** (steps / 12))

def adsr(duration, attack=0.01, decay=0.1, sustain=0.7, release=0.1):
    """Return an ADSR envelope as a numpy array."""
    n = int(SR * duration)
    env = np.zeros(n)

    a = int(SR * attack)
    d = int(SR * decay)
    r = int(SR * release)
    s = n - a - d - r

    env[:a]         = np.linspace(0, 1, a)           # attack
    env[a:a+d]      = np.linspace(1, sustain, d)      # decay
    env[a+d:a+d+s]  = sustain                         # sustain
    env[a+d+s:]     = np.linspace(sustain, 0, r)      # release
    return env



# A minor scale starting at A3 (220 Hz)
# Steps: 0, 2, 3, 5, 7, 8, 10, 12
A4 = 440.0
scale_steps = [0, 2, 3, 5, 7, 8, 10, 12]

melody = np.concatenate([
    note(semitones(A4, s), 0.4) for s in scale_steps
])
play(melody)
save(melody, "scale.wav")