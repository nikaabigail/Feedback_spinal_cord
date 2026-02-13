import numpy as np
from ...core.types import StimChannelParams

def preview_wave(ch: StimChannelParams, ms: float = 80.0, fs: int = 2000):
    t = np.linspace(0, ms/1000.0, int(fs*ms/1000.0), endpoint=False)
    y = np.zeros_like(t)

    if (not ch.enabled) or ch.frequency <= 0 or ch.amplitude == 0:
        return t, y

    wf = getattr(ch, "waveform", "rect_biphasic")

    if wf == "sine":
        y = ch.amplitude * np.sin(2*np.pi*ch.frequency*t)

    elif wf == "rect":
        y = ch.amplitude * (np.sin(2*np.pi*ch.frequency*t) > 0).astype(float)

    elif wf == "rect_biphasic":
        pw = float(getattr(ch, "pulse_width_us", 200.0)) / 1e6
        ip = float(getattr(ch, "interphase_us", 50.0)) / 1e6
        period = 1.0 / ch.frequency
        for k in range(int(t[-1] // period) + 3):
            t0 = k * period
            a = (t >= t0) & (t < t0 + pw)
            b = (t >= t0 + pw + ip) & (t < t0 + pw + ip + pw)
            y[a] =  ch.amplitude
            y[b] = -ch.amplitude

    return t, y
