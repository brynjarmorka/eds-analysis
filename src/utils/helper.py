# general helper functions

#
#
# linmap_kev_to_index and linmap_index_to_kev BELOW ARE WRONG !!!
#
#


def linmap_kev_to_index(kev):
    """
    Convert keV to index, assuming a linear mapping of 2048 points from 0 to 20 keV.
    Input the keV you want to convert.

    Returns: int with the index.
    """
    return int(kev * 2048 / 20)


def linmap_index_to_kev(index):
    """
    Convert index to keV, assuming a linear mapping of 2048 points from 0 to 20 keV.
    Input the index you want to convert.

    NB! remember the channel width

    Returns: float with the keV.
    """
    return float(index * 20 / 2048)


# everything above this line runs on import,
# while everything below this line only runs when get_raw_data.py is called
if __name__ == "__main__":
    print("You just ran the module 'helper.py'")
