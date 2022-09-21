"""
This is a helper file for extracting the raw data from the .emsa files.
The functions can return the raw data or plot a simple spectrum.
"""
#%%
import hyperspy.api as hs
from pathlib import Path
import numpy as np


def get_emsa_dir():
    """
    Reads the "~/.eds_analysis" file in your HOMEdir to get the path to the emsa files.
    If there is no file, a default FileNotFoundError get raised.
    get_emsa_dir() assumes that the .eds_analysis contains only the path, with eventually some whitespace.

    Returns: string

    """
    # Accessing the HOME dir of the user
    path = Path("~/.eds_analysis").expanduser()
    f = open(path, "r")
    local_path = f.read()
    # Removes any potential newlines in the file
    local_path = local_path.replace("\n", "")
    f.close()
    return local_path


def locate_raw_data():
    """
    Locate the raw data folder.

    Returns: list of strings with the full paths to the .emsa files.

    """
    exports = Path(get_emsa_dir())
    emsa_paths = list(exports.glob("*.emsa"))
    # print(f"{len(emsa_paths)} .emsa files ready in list given by locate_raw_data().")
    return emsa_paths


# I guess I could just always normalize to the highest peak,
# since the counts are more or less arbitrary anyway.
# If I do not want to normalize, I need to send normalize through many func.
# Also, normalize will not affect hspy plotting.
def get_raw_data_array(filenr, normalize=True):
    """
    Get the raw data from a hspy file as a numpy array.
    Input the filenumber you want to get the data from.

    Returns: np.array with the raw data, shape = (2048,).

    """
    emsa_paths = locate_raw_data()
    s = hs.load(emsa_paths[filenr], signal_type="EDS_SEM")
    # normalize to the highest peak
    if normalize:
        return s.data / s.data.max()
    return s.data


def get_raw_data_array_from_filename(filename, normalize=True):
    """
    Get the raw data from a hspy file as a numpy array.
    Input the whole filename you want to get the data from.

    Returns: np.array with the raw data, shape = (2048,).

    """
    s = hs.load(filename, signal_type="EDS_SEM")
    # normalize to the highest peak
    if normalize:
        return s.data / s.data.max()
    return s.data


# get_raw_data_array(-1).max()  # developing


def sum_multiple_data_arrays(arrays, normalize=False):
    """
    Sum multiple data arrays from the raw data.
    Can normalize the data by dividing by the number of arrays summed.

    Returns: Summed data_array, and eventually their names in a string
    """
    summed = np.zeros(2048)
    names = ""
    for i in range(len(arrays)):
        names += arrays[i][0] + ", "
        summed += arrays[i][1]
    names = names[:-2]  # removing the last comma
    print(f"Summed {len(arrays)} arrays: {names}")
    if normalize:
        return summed / len(arrays), names
    else:
        return [names, summed]


def get_multiple_data_arrays(filters=[], every=False):
    """
    Get multiple data arrays from the raw data, with a filter on the filenames.

    Returns: 2d list, [emsa.stem, data_array]
    """
    emsa_array = []
    emsa_paths = locate_raw_data()
    # when returning all
    if every:
        for i in range(len(emsa_paths)):
            emsa_array.append(
                [
                    emsa_paths[i].stem,
                    get_raw_data_array_from_filename(emsa_paths[i], normalize=True),
                ]
            )
        return emsa_array
    # when filtering
    for filename in emsa_paths:
        for flt in filters:
            if flt in filename.stem:
                emsa_array.append(
                    [
                        filename.stem,
                        get_raw_data_array_from_filename(filename, normalize=True),
                    ]
                )
    return emsa_array


#%%
# everything above this line runs on import,
# while everything below this line only runs when get_raw_data.py is called
if __name__ == "__main__":
    print("You just ran the module 'get_raw_data.py'")
