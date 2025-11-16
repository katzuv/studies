def normalize_ticks(ticks):
    peak_indices, _ = scipy.signal.find_peaks(ticks)
    peak_average = np.average(ticks[peak_indices])
    valley_indices, _ = scipy.signal.find_peaks(-ticks)
    valley_average = -np.average(ticks[valley_indices])

    mid = (peak_average + valley_average) / 2
    return ticks - mid

