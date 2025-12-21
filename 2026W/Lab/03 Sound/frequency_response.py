import numpy as np
import scipy
from matplotlib import pyplot as plt

freq = np.array(
    (3700, 3800, 3900, 4000, 4100, 4160, 4211, 4310, 4410, 4500, 4600, 4700, 4800, 4900, 5000, 4130, 4190, 4210, 4240,
     4270, 4330, 4370, 4180))
freq_err = np.array((10, 10, 10, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 10, 20, 20, 20, 10, 20, 20, 20, 20))  # Hz
amp = np.array((2, 3, 4, 6.8, 13, 23.5, 32, 25, 15, 12, 9, 8, 7, 6, 5.5, 18.2, 28, 32, 30, 28, 22, 18.5, 27))
amp_err = np.array(
    (1, 1.5, 2, 1, .5, 1, 1, 1, 1.5, 2, 1.5, 1.5, 2, 1.5, 2, 2, 2, 1.5, 2, 2, 2, 2, 2)) / 1000  # mV +- 0.05
plt.errorbar(freq, amp, xerr=10, yerr=amp_err, fmt='.', label="Data")

peak_indices, _ = scipy.signal.find_peaks(amp)
highest_peaks_indices = sorted(peak_indices, key=lambda i: amp[i], reverse=True)
plt.plot(freq[highest_peaks_indices], amp[highest_peaks_indices], "^", label="Max amplitude", zorder=3)

# Annotate top peaks and include their frequencies in the marker label
x_rng = freq.max() - freq.min() if freq.size else 1.0
y_rng = amp.max() - amp.min() if amp.size else 1.0
for idx in highest_peaks_indices:
    x = freq[idx]
    y = amp[idx]
    xerr = freq_err[idx]
    yerr = amp_err[idx]
    f_khz = x / 1000.0
    text = f"{y} ± {yerr:.3f} mV\nat {f_khz:.2f} Hz"
    # lower-left box and a curved arrow for a prettier look
    xytext = (x - 0.15 * x_rng, y - 0.25 * y_rng)
    plt.annotate(
        text,
        xy=(x, y),
        xytext=xytext,
        ha='right',
        va='top',
        arrowprops=dict(arrowstyle='->', color='red', lw=1.2, connectionstyle='arc3,rad=-0.4'),
        bbox=dict(boxstyle='round,pad=0.4', fc='white', alpha=0.95),
        fontsize=9,
        zorder=4,
    )

plt.legend()
plt.xlabel('Frequency [Hz]')
plt.ylabel('Amplitude [mV]')
plt.grid()
plt.savefig("freq_response.svg", format="svg")
plt.show()
