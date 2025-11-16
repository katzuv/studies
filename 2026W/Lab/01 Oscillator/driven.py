def normalize_ticks(ticks):
    peak_indices, _ = scipy.signal.find_peaks(ticks)
    peak_average = np.average(ticks[peak_indices])
    valley_indices, _ = scipy.signal.find_peaks(-ticks)
    valley_average = -np.average(ticks[valley_indices])

    mid = (peak_average + valley_average) / 2
    return ticks - mid


def amplitude_ratio_model(frequency, spring_constant, mass, natural_frequency, tau):
    under_root = (natural_frequency ** 2 - frequency ** 2) ** 2 + (frequency / tau) ** 2
    return (spring_constant / mass) * 1 / np.root(under_root)

