import numpy as np
import plotly.graph_objects as go
from scipy.signal import find_peaks
from scipy.optimize import curve_fit
from helper_files.gaussian_fitting import gaussian


# TODO: Add docstrings


def split_arrs(data):
    arrs = []
    names = []
    for d in data:
        arrs.append(d[1])
        names.append(d[0])
    return arrs, names


def channel_to_kev(
    value=None, arr=None, dispersion=0.0100283, offset=21.078, use_offset=True
):
    if not use_offset:
        offset = 0
    if value is not None:
        return (value - offset) * dispersion
    if arr is not None:
        return (np.array(arr) - offset) * dispersion
    else:
        raise ValueError("No value or array provided to chennel_to_keV(...)")


def find_peaks_arrs(data, prominence):
    peaks = []
    for d in data:
        peak, _ = find_peaks(d, prominence=prominence)
        peaks.append(peak)
    return peaks

    # linear background removal, from the peak +- k channels


def remove_linear_bg(y, peaks, pixel_removal=40, offset=10):
    bg = y.copy()
    for p in peaks:
        # if the peak is too close to the edge, just say the bg is 0
        if p < pixel_removal:
            bg[:p] = 0
            continue
        else:
            bg[p - pixel_removal : p + pixel_removal] = np.nan
    # make linear interpolation between nan values
    bg = np.interp(np.arange(len(bg)), np.flatnonzero(~np.isnan(bg)), bg[~np.isnan(bg)])

    bg[: int(offset)] = 0  # first 10 channels or the offset should be 0
    return bg


def n_gaussians_and_m_order_bg(x, deg, *args, high_res=False, res_increase=10):
    poly = args[: deg + 1]
    gauss = args[deg + 1 :]
    if high_res:
        x = np.linspace(x[0], x[-1], len(x) * res_increase)
    n = int(len(gauss) / 3)
    y = np.zeros(len(x))
    for i in range(n):
        y += gaussian(x, gauss[3 * i], gauss[3 * i + 1], gauss[3 * i + 2])
    y += np.polyval(poly, x)
    if high_res:
        y = y[res_increase // 2 :]  # chop off the first half of res_increase values
    return y


# putting it into one function
def make_fit(array, x, deg=12, prominence=0.01, pixel_removal=50, offset=20):
    # fits one array to n gaussians and a m order polynomial
    peaks, _ = find_peaks(array, prominence=prominence)
    std = np.ones(len(peaks))
    amp = np.ones(len(peaks))

    # must define the function to cure_fit, since deg is a variable which is not allowed in the function,
    # because it is not a parameter of the function that curve_fit is trying to fit
    def fit_func_peaks_and_bg(x, *args):
        poly = args[: deg + 1]
        gauss = args[deg + 1 :]
        n = int(len(gauss) / 3)
        y = np.zeros(len(x))
        for i in range(n):
            y += gaussian(x, gauss[3 * i], gauss[3 * i + 1], gauss[3 * i + 2])
        y += np.polyval(poly, x)
        return y

    # removing the background linearly for an initial guess of the polynomial
    bg = remove_linear_bg(array, peaks, pixel_removal=pixel_removal, offset=offset)
    # fitting the polynomial
    poly_init = np.polyfit(x, bg, deg)

    # fitting
    init_vals = list(poly_init)
    for i in range(len(peaks)):
        init_vals += [amp[i], peaks[i], std[i]]
    fit_vals, covar = curve_fit(fit_func_peaks_and_bg, x, array, p0=init_vals)

    return (fit_vals, covar)


def find_nearest(array, value):
    # gives index of the value in array that is closest to value
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx


def fwhm(std):
    # (std*2*sqrt(2*ln(2)))
    # fFWHM defined as in: https://en.wikipedia.org/wiki/Full_width_at_half_maximum"
    return std * 2 * np.sqrt(2 * np.log(2))


def print_table(header, table, delim="&"):
    head = ""
    for h in header:
        head += f"{h:<16} {delim} "
    print(head)
    for row in table.T:
        row_str = ""
        for r in row:
            try:
                row_str += f"{float(r):<16.3f} {delim} "
            except:
                row_str += f"{r:<16} {delim} "
        print(row_str)


def plotly_table(header, table, Vacc):
    fig = go.Figure(
        data=[go.Table(header=dict(values=header), cells=dict(values=table))]
    )
    fig.update_layout(
        title=f"{Vacc} kV, peak ratios after fitting and background subtraction"
    )
    fig.show()


def table_values_FWHM(peaks_keV, peaks_high_res, stds_keV):
    # gives table with values, FWHM and area of each peak
    p_area = [sum(peaks_high_res[i]) for i in range(len(peaks_keV))]
    p_fwhm = [fwhm(stds_keV[i]) * 1000 for i in range(len(peaks_keV))]

    header = ["Peak value [keV]", "FWHM [eV]", "Area [a.u.]"]
    table = np.array([peaks_keV, p_fwhm, p_area])
    return header, table
