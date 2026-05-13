import numpy as np
import pygame
import time

SR = 44100

def bjorklund(beats, slots):
    """Return a Euclidean rhythm as a list of 0s and 1s."""
    if beats == 0:
        return [0] * slots
    if beats == slots:
        return [1] * slots

    pattern    = [[1]] * beats + [[0]] * (slots - beats)
    remainder  = slots - beats

    while remainder > 1:
        times = min(len(pattern) - remainder, remainder)
        for i in range(times):
            pattern[i] = pattern[i] + pattern[-(i+1)]
        pattern = pattern[:len(pattern)-times]
        remainder = len(pattern) - times
        if remainder <= 0:
            break

    return [x for group in pattern for x in group]

def make_click(freq, duration=0.05, sr=SR):
    """Simple sine burst for a drum sound."""
    t    = np.linspace(0, duration, int(sr * duration))
    wave = np.sin(2 * np.pi * freq * t) * np.exp(-t * 40)
    return (wave * 32767).astype(np.int16)

def play_euclidean(beats, slots, bpm=120, bars=4, freq=200):
    """Play a Euclidean rhythm."""
    pattern  = bjorklund(beats, slots)
    step_dur = 60 / (bpm * slots / 4)   # duration of one slot in seconds

    pygame.mixer.init(frequency=SR, size=-16, channels=1, buffer=512)
    click = make_click(freq)
    sound = pygame.sndarray.make_sound(click)

    print(f"E({beats},{slots}): {pattern}")

    for _ in range(bars):
        for hit in pattern:
            if hit:
                sound.play()
            time.sleep(step_dur)

    pygame.mixer.quit()

# ── Try these classic Euclidean rhythms ───────────────────────────────────────
print("Tresillo (3,8) — Cuban son")
play_euclidean(3, 8, bpm=120, freq=180)

print("Cinquillo (5,8) — Cuban/African")
play_euclidean(5, 8, bpm=120, freq=220)

print("Bossa nova (3,16) — Brazilian")
play_euclidean(3, 16, bpm=100, freq=160)

print("E(4,4)")
play_euclidean(4, 4, bpm=100, freq=160)

print("E(1,8)")
play_euclidean(1, 8, bpm=100, freq=160)

