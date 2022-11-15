# different types of normalization
import numpy as np

# normalize to 1 for the highest peak in each spectrum
def normalize_high_peak(data):
    # data = [[name, data], [name, data], ...]
    # needs to be a copy, otherwise it will change the original data
    normalized = [item.copy() for item in data]
    for i in range(len(normalized)):
        normalized[i][1] = normalized[i][1] / np.max(normalized[i][1])
    return normalized


# normalize to the total counts in each spectrum
def normalize_total_counts(data):
    # data = [[name, data], [name, data], ...]
    # needs to be a copy, otherwise it will change the original data
    normalized = [item.copy() for item in data]
    for i in range(len(normalized)):
        normalized[i][1] = normalized[i][1] / np.sum(normalized[i][1])
    return normalized


# normalize to the counts in the zero peak
def normalize_zero_peak(data, zp_start=16, zp_stop=27):
    # data = [[name, data], [name, data], ...]
    # needs to be a copy, otherwise it will change the original data
    normalized = [item.copy() for item in data]
    for i in range(len(normalized)):
        zp_counts = np.sum(normalized[i][1][zp_start:zp_stop])
        # print(zp_counts)
        normalized[i][1] = normalized[i][1] / zp_counts
    return normalized


# normalize to the cps noted down while taking the data
def normalize_cps(data, cps):
    # needs to be a copy, otherwise it will change the original data
    normalized = [item.copy() for item in data]
    for i in range(len(normalized)):
        normalized[i][1] = normalized[i][1] / cps[i]
    return normalized


# normalize to the dead time
def normalize_dt(data, dt):
    # needs to be a copy, otherwise it will change the original data
    normalized = [item.copy() for item in data]
    for i in range(len(normalized)):
        normalized[i][1] = normalized[i][1] / dt[i]
    return normalized


# normalize to a section of the background
def normalize_bg(data, bg_start=80, bg_stop=100):
    # needs to be a copy, otherwise it will change the original data
    normalized = [item.copy() for item in data]
    for i in range(len(normalized)):
        normalized[i][1] = normalized[i][1] / np.sum(normalized[i][1][bg_start:bg_stop])
    return normalized
