import numpy as np
from scipy.optimize import curve_fit


def gaussian(x, mean, std=1, amp=1):
    ###### endre rekkefølge i de som bruker gaussian!
    """
    Makes a gaussian function with the given parameters.

    1/(std * np.sqrt(2 * np.pi)) * np.exp(- (x - mean)**2 / (2 * std**2))

    Parameters
    ----------
    x : list or np.array
        The channel values where the gaussian is made.
    amp : int or float
        Amplitude of the gaussian. Normaly (1/(sigma * sqrt(2*pi))), but 1 is fine.
    cen : int or float
        Center of the gaussian, where the peak is.
    wid : int or float
        Width of the gaussian.

    Returns
    -------
    List or np.array
        The gaussian function with the given parameters over the given x values.
    """
    # (1 / (std * np.sqrt(2 * np.pi)))
    return amp * np.exp(-((x - mean) ** 2) / (2 * std**2))


def two_gaussians(x, mean1, std1, amp1, mean2, std2, amp2):
    """
    Generates a sum of two gaussians, if you know two peaks are close/overlap.
    Uses the gaussian function.

    Parameters
    ----------
    x : list or np.array
        The channel values where the gaussian is made, must cover both peaks.
    amp1 : int or float
        Amplitude of the first gaussian.
    cen1 : int or float
        Center of the first gaussian, where the peak is.
    1 : int or float
        Width of the first gaussian.
    amp2 : int or float
        Amplitude of the second gaussian.
    cen2 : int or float
        Center of the second gaussian, where the peak is.
    wid2 : int or float
        Width of the second gaussian.

    Returns
    -------
    List or np.array
        The two gaussian function with the given parameters over the given x values.
    """
    return gaussian(x, mean1, std1, amp1) + gaussian(x, mean2, std2, amp2)


def n_gaussians(x, *args):
    """
    Generates a sum of n gaussians, if you know n peaks are in the spectrum.
    Uses the gaussian function.

    Parameters
    ----------
    x : list or np.array
        The channel values where the gaussian is made, must cover all peaks.
    *args : list or np.array
        The parameters for the gaussians, must be in the order:
        [mean1, std1, amp1, mean2, std2, amp2, ...]

    Returns
    -------
    List or np.array
        The n gaussian function with the given parameters over the given x values.
    """
    n = int(len(args) / 3)
    y = np.zeros(len(x))
    for i in range(n):
        y += gaussian(x, args[3 * i], args[3 * i + 1], args[3 * i + 2])
    return y


def fit_peak_to_gaussian(
    raw_y,
    guess_peak,
    buffer=50,
    start=None,
    stop=None,
    guess_std=1,
    guess_amp=1,
    give_xy=True,
):
    """
    Fits a peak to a gaussian, given an array and the guessed center.
    If no start and stop are given, it use the guess +- buffer channels.
    Returns either the estimated [x, y_est] or the fitted param [[mean, std], covar].

    Parameters
    ----------
    raw_y : np.array
        The raw data of the spectrum with one peak.
    guess : int or float
        Inital guess of the center of the peak.
    buffer : int, optional
        Fitting area in channels around the peak if start and/or stop is None, by default 50
    start : int, optional
        Start of the fitting area, by default None
    stop : int, optional
        Stop of the fitting area, by default None
    guess_amp : int, optional
        Initial guess of the amplitude, and not that important, by default 1
    guess_wid : int, optional
        Initial guess of the width, and not that important, by default 1
    give_xy : bool, optional
        Deciding the output version, see below, by default True

    Returns
    -------
    np.array
        Either the estimated [x, y_est] or the fitted param [[mean, std], covar].
    """
    if not start:
        start = guess_peak - buffer
    if not stop:
        stop = guess_peak + buffer
    x = np.arange(start, stop, 1)
    y = raw_y[0][1][start:stop]
    # the initial guess is the center, the amplitude and the width of the peak
    init_vals = [guess_peak, guess_std, guess_amp]
    fit_vals, covar = curve_fit(gaussian, x, y, p0=init_vals)

    y_est = gaussian(x, fit_vals[0], fit_vals[1], fit_vals[2])

    if give_xy:
        return [x, y_est]
    else:
        return [fit_vals, covar]


def fit_two_peaks_to_two_gaussians(
    raw_y,
    guesses_peaks,
    buffer=50,
    start=None,
    stop=None,
    guess_std=1,
    guess_amp=1,
    give_xy=True,
):
    """
    Fits two peaks to two gaussians, given an array and the guessed centers.
    If no start and stop are given, it use the guess +- buffer channels.
    Returns either the estimated [x, y_est] or the fitted param [[amp, cen, wid], covar].

    Parameters
    ----------
    raw_y : np.array
        The raw data of the spectrum with one peak.
    guesses : list or np.array of int
        Inital guesses of the two centers of the peak.
    buffer : int, optional
        Fitting area in channels around the peak if start and/or stop is None, by default 50
    start : int, optional
        Start of the fitting area, by default None
    stop : int, optional
        Stop of the fitting area, by default None
    guess_amp : int, optional
        Initial guess of the amplitude, and not that important, by default 1
    guess_wid : int, optional
        Initial guess of the width, and not that important, by default 1
    give_xy : bool, optional
        Deciding the output version, see below, by default True

    Returns
    -------
    np.array
        Either the estimated [x, y_est] or the fitted param [[amp, cen, wid], covar].
    """
    if not start:  # if not None
        start = min(guesses_peaks) - buffer
    if not stop:
        stop = max(guesses_peaks) + buffer
    x = np.arange(start, stop, 1)
    y = raw_y[0][1][start:stop]
    # the initial guess is the center, the amplitude and the width of the peak
    init_vals = [
        guesses_peaks[0],
        guess_std,
        guess_amp,
        guesses_peaks[1],
        guess_std,
        guess_amp,
    ]
    fit_vals, covar = curve_fit(two_gaussians, x, y, p0=init_vals)

    y_est = two_gaussians(
        x, fit_vals[0], fit_vals[1], fit_vals[2], fit_vals[3], fit_vals[4], fit_vals[5]
    )

    if give_xy:
        return [x, y_est]
    else:
        return [fit_vals, covar]


def fit_n_peaks_to_gaussian(
    raw_y,
    guesses_peaks,
    guesses_std=1,
    guesses_amp=1,
    give_xy=True
):
    """
    Fits n peaks to n gaussians, given an array and the guessed centers.
    If no start and stop are given, it use the guess +- buffer channels.
    Returns the fitted param [[amp, cen, wid], covar].

    Parameters
    ----------
    raw_y : np.array
        The raw y data of the spectrum with n peaks
    guesses_peaks : list or np.array of int
        Inital guesses of the n peaks ()
    guesses_amp : int, optional
        Initial guess of the amplitude, and not that important, by default 1
    guess_wid : int, optional
        Initial guess of the width, and not that important, by default 1
    give_xy : bool, optional
        Deciding the output version, see below, by default True
    Returns
    -------
    np.array
        The gaussian fitted xy_vals, or
        The fitted param [[amp, cen, wid], covar].
    """
    if guesses_std == 1:
        guesses_std = np.ones(len(guesses_peaks))
    if guesses_amp == 1:
        guesses_amp = np.ones(len(guesses_peaks))
    x2048 = np.arange(0, 2048, 1)
    for i in range(len(guesses_peaks)):
        if i == 0:
            init_vals = [guesses_peaks[i], guesses_std[i], guesses_amp[i]]
        else:
            init_vals += [guesses_peaks[i], guesses_std[i], guesses_amp[i]]
    fit_vals, covar = curve_fit(n_gaussians, x2048, raw_y, p0=init_vals)

    if give_xy:
        return [x2048, n_gaussians(x2048, *fit_vals)]
    else:
        return [fit_vals, covar]
