from sound_base import *

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
wet = echo(dry, delay_seconds=0.05, decay=0.8)

play(dry)
play(wet)
save(wet, "echo.wav")