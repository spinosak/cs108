from sound_base import *

def reverb(wave, room_size=0.3, num_reflections=80):
    output = wave.copy().astype(np.float64)
    max_delay = int(SR * room_size)
    for _ in range(num_reflections):
        delay   = np.random.randint(100, max_delay)
        decay   = np.random.uniform(0.1, 0.4)
        pad     = np.zeros(delay)
        reflect = np.concatenate([pad, wave * decay])
        if len(reflect) > len(output):
            output = np.concatenate([output, np.zeros(len(reflect) - len(output))])
        output[:len(reflect)] += reflect
    return output / np.max(np.abs(output)) * 0.8

dry  = note(440, 1.0, amplitude=0.5)
wet  = reverb(dry, room_size=0.3)
cave = reverb(dry, room_size=1.5, num_reflections=200)

play(dry)
play(wet)
play(cave)
save(cave, "reverb.wav")
