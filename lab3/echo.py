from sound_base import *

def echo(wave, delay_seconds=0.3, decay=0.5, num_echoes=4):
    delay_samples = int(SR * delay_seconds)
    output = wave.copy()
    for i in range(1, num_echoes + 1):
        pad    = np.zeros(delay_samples * i)
        echo_i = np.concatenate([pad, wave * (decay ** i)])
        # match lengths
        if len(echo_i) > len(output):
            output = np.concatenate([output, np.zeros(len(echo_i) - len(output))])
        output[:len(echo_i)] += echo_i
    return output / np.max(np.abs(output)) * 0.8

dry = np.concatenate([note(440, 0.3), np.zeros(int(SR * 0.5)),
                      note(550, 0.3), np.zeros(int(SR * 0.5))])
wet = echo(dry, delay_seconds=0.8, decay=0.5)

play(dry)
play(wet)
save(wet, "echo.wav")