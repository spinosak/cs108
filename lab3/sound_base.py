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

# Sine 

def sine(freq, duration, amplitude=0.3):
    t = timeline(duration)
    return amplitude * np.sin(2 * np.pi * freq * t)

# Note
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

# Semitones
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

# chords
def chord(freqs, duration, amplitude=0.25):
    waves = [note(f, duration, amplitude) for f in freqs]
    mixed = sum(waves)
    return mixed / np.max(np.abs(mixed)) * amplitude


def kick(duration=0.4):
    """Low thump — a sine wave that drops in pitch quickly."""
    t = timeline(duration)
    freq_env = np.exp(-t * 20) * 150 + 50   # pitch drops from 200 to 50 Hz
    wave = np.sin(2 * np.pi * np.cumsum(freq_env) / SR)
    env  = np.exp(-t * 10)
    return 0.8 * wave * env

def snare(duration=0.2):
    """Snappy noise burst — filtered white noise."""
    t = timeline(duration)
    noise = np.random.uniform(-1, 1, len(t))
    env   = np.exp(-t * 20)
    return 0.5 * noise * env

def hihat(duration=0.05):
    """Short high noise click."""
    t = timeline(duration)
    noise = np.random.uniform(-1, 1, len(t))
    env   = np.exp(-t * 60)
    return 0.3 * noise * env

def place(sound, position_seconds, total_length_seconds):
    """Place a sound at a position in a longer buffer."""
    buf   = np.zeros(int(SR * total_length_seconds))
    start = int(SR * position_seconds)
    end   = start + len(sound)
    if end <= len(buf):
        buf[start:end] += sound
    return buf
