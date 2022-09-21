#%%
import numpy as np

# my modules
from getting_spectral_lines_from_hspy import get_the_lines_from_hspy
from get_raw_data import locate_raw_data, get_raw_data_array
from helper import linmap_kev_to_index, linmap_index_to_kev

from helper_plotting import (
    simple_hspy_plot,
    simple_matplotlib_plot,
    simple_plot_with_lines,
)

#%%

# developing
# remove the variables below when done, so they dont get imported

# dictionary with the lines from hspy
lines = get_the_lines_from_hspy()
# list of raw data paths, which are inputs to the functions below
emsa_paths = locate_raw_data()


def locate_max_value(filenr, kev=False, start=0, stop=2048):
    """
    Locate the index and keV of maximum value in a range of the raw data.
    Input the filenumber you want to get the data from.
    Input the start and stop in [keV] of the range you want to search in.

    Returns: integer channel number of the maximum value in the range.
    """
    # mapping start and stop from keV to the index of the raw data
    # TODO: calibrate the mapping in linmap_kev_to_index() !!!
    raw_data = get_raw_data_array(filenr)
    if kev:
        start = linmap_kev_to_index(start)  # NOT WORKING !!!
        stop = linmap_kev_to_index(stop)  # NOT WORKING !!!
    max_index = np.argmax(raw_data[start:stop])
    return max_index + start  # + start to compensate for shorter list


def calibrate_linear_channel_width(filenr, line1, line2, kev=False, range=100):
    """
    Calibrate the channel width.
    Input the filenumber you want to get the data from.
    Input the two X-ray lines you want to calibrate between in [keV].
    Range is to buffer up the search area for the max value from the lines.

    Returns: float with the calibrated channel width.
    """
    # conversion from keV to index, just to hit the right range for peak search
    conversion = 105
    # raw_data = get_raw_data_array(filenr)
    line1_apporx_channel = int(line1 * conversion)
    line2_approx_channel = int(line2 * conversion)
    # print(line1_apporx_channel, line2_approx_channel)
    line1_raw = locate_max_value(
        filenr, start=line1_apporx_channel - range, stop=line1_apporx_channel + range
    )
    line2_raw = locate_max_value(
        filenr, start=line2_approx_channel - range, stop=line2_approx_channel + range
    )
    # print(line1_raw, line2_raw)
    delta_e = line2 - line1
    delta_channel = line2_raw - line1_raw
    print(f"Calibrated channel width: {delta_e / delta_channel} keV/channel\n")
    return delta_e / delta_channel


#%%
def calibrate_with_Mo_la_ka():
    """
    Calibrate the channel width with Mo L-alpha and K-alpha.
    """
    la = lines["Mo"]["La"]["energy (keV)"]
    ka = lines["Mo"]["Ka"]["energy (keV)"]
    print(f"From Mo_30kV using L-alpha: {la} keV and K-alpha: {ka} keV")
    # using file 10, Mo_30keV
    return calibrate_linear_channel_width(10, la, ka)


def calibrate_with_Ga_la_ka():
    """
    Calibrate the channel width with Ga K-alpha and Ga L-alpha.
    """
    la = lines["Ga"]["La"]["energy (keV)"]
    ka = lines["Ga"]["Ka"]["energy (keV)"]
    print(f"From GaAs_30kV using L-alpha: {la} keV and K-alpha: {ka} keV")
    # using file 10, Mo_30keV
    return calibrate_linear_channel_width(6, la, ka)


def calibrate_with_As_la_ka():
    """
    Calibrate the channel width with As K-alpha and As K-beta.
    """
    ka = lines["As"]["Ka"]["energy (keV)"]
    kb = lines["As"]["Kb"]["energy (keV)"]
    print(f"From GaAs_30kV using L-alpha: {ka} keV and K-alpha: {kb} keV")
    # using file 10, Mo_30keV
    return calibrate_linear_channel_width(6, ka, kb)


cmo = calibrate_with_Mo_la_ka()
cga = calibrate_with_Ga_la_ka()
cas = calibrate_with_As_la_ka()

print(f"Mo calib: {cmo}")
print(f"Ga calib: {cga}")
print(f"As calib: {cas}")


#%%
#
#
#
# TODO: funcs for later
#
#
#


def locate_max_value_around_theoretical_line(filenr, line, kev=False, range=50):
    """
    Locate the maximum value around a theoretical line.
    Input the filenumber you want to get the data from.
    Input the line you want to search around.
    Input if you want to search in [keV] or [index].
    Input the range around the line you want to search in channel numbers.

    Returns: float with the maximum value in the range.
    """
    # mapping start and stop from keV to the index of the raw data
    # raw_data = get_raw_data_array(filenr)
    if kev:
        range = linmap_kev_to_index(range)
    return locate_max_value(filenr, start=line - range, stop=line + range)


def validate_if_max_value_is_a_peak(filenr, value_array):
    """
    Validate if the max value is a peak.
    Input the filenumber you want to get the data from.
    Input the value array from locate_max_value().

    Returns: bool if the max value is a peak.
    """
    ...


# %%

# everything above this line runs on import,
# while everything below this line only runs when get_raw_data.py is called
if __name__ == "__main__":
    print("You just ran the module 'channel_width_calibration.py'")
