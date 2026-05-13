import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
from scipy.signal import butter, lfilter
import matplotlib.pyplot as plt

SR = 44100  # samples per second — standard CD quality

# ── Playback ──────────────────────────────────────────────────────────────────
def play(wave):
    """Play a numpy array as audio."""
    sd.play(wave.astype(np.float32), SR)
    sd.wait()

# ── Save ─────────────────────────────────────────────────────────────────────
def save(wave, filename):
    """Save a numpy array as a 16-bit WAV file."""
    normalized = np.int16(wave / np.max(np.abs(wave)) * 32767)
    write(filename, SR, normalized)
    print(f"Saved: {filename}")

# ── Visualize ─────────────────────────────────────────────────────────────────
def show(wave, title="", duration=0.05):
    """Plot the first `duration` seconds of a wave."""
    samples = int(SR * duration)
    plt.figure(figsize=(10, 2))
    plt.plot(wave[:samples], linewidth=0.8)
    plt.title(title)
    plt.xlabel("samples")
    plt.ylabel("amplitude")
    plt.tight_layout()
    plt.show()

# ── Time axis ─────────────────────────────────────────────────────────────────
def timeline(duration):
    """Return a time array for a given duration in seconds."""
    return np.linspace(0, duration, int(SR * duration))

# ── Sine ──────────────────────────────────────────────────────────────────────
def sine(freq, duration, amplitude=0.3):
    t = timeline(duration)
    return amplitude * np.sin(2 * np.pi * freq * t)

# ── Extra ──────────────────────────────────────────────────────────────────────
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

def chord(freqs, duration, amplitude=0.25):
    waves = [note(f, duration, amplitude) for f in freqs]
    mixed = sum(waves)
    return mixed / np.max(np.abs(mixed)) * amplitude
