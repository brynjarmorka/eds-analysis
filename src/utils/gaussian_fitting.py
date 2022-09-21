import numpy as np
from scipy.optimize import curve_fit


def gaussian(x, amp, cen, wid):
    """
    Makes a gaussian function with the given parameters.

    Parameters
    ----------
    x : list or np.array
        The channel values where the gaussian is made.
    amp : int or float
        Amplitude of the gaussian.
    cen : int or float
        Center of the gaussian, where the peak is.
    wid : int or float
        Width of the gaussian.

    Returns
    -------
    List or np.array
        The gaussian function with the given parameters over the given x values.
    """
    return amp * np.exp(-((x - cen) ** 2) / wid)


def two_gaussians(x, amp1, cen1, wid1, amp2, cen2, wid2):
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
    return gaussian(x, amp1, cen1, wid1) + gaussian(x, amp2, cen2, wid2)


def fit_peak_to_gaussian(
    raw_y,
    guess,
    buffer=50,
    start=None,
    stop=None,
    guess_amp=1,
    guess_wid=1,
    give_xy=True,
):
    """
    Fits a peak to a gaussian, given an array and the guessed center.
    If no start and stop are given, it use the guess +- buffer channels.
    Returns either the estimated [x, y_est] or the fitted param [[amp, cen, wid], covar].

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
        Either the estimated [x, y_est] or the fitted param [[amp, cen, wid], covar].
    """
    if not start:
        start = guess - buffer
    if not stop:
        stop = guess + buffer
    x = np.arange(start, stop, 1)
    y = raw_y[0][1][start:stop]
    # the initial guess is the center, the amplitude and the width of the peak
    init_vals = [guess_amp, guess, guess_wid]
    fit_vals, covar = curve_fit(gaussian, x, y, p0=init_vals)

    y_est = gaussian(x, fit_vals[0], fit_vals[1], fit_vals[2])

    if give_xy:
        return [x, y_est]
    else:
        return [fit_vals, covar]


def fit_two_peaks_to_two_gaussians(
    raw_y,
    guesses,
    buffer=50,
    start=None,
    stop=None,
    guess_amp=1,
    guess_wid=1,
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
        start = min(guesses) - buffer
    if not stop:
        stop = max(guesses) + buffer
    x = np.arange(start, stop, 1)
    y = raw_y[0][1][start:stop]
    # the initial guess is the center, the amplitude and the width of the peak
    init_vals = [guess_amp, guesses[0], guess_wid, guess_amp, guesses[1], guess_wid]
    fit_vals, covar = curve_fit(two_gaussians, x, y, p0=init_vals)

    y_est = two_gaussians(
        x, fit_vals[0], fit_vals[1], fit_vals[2], fit_vals[3], fit_vals[4], fit_vals[5]
    )

    if give_xy:
        return [x, y_est]
    else:
        return [fit_vals, covar]
