#
## There is definetly a better way to do this, but ill just roll with this now
#

# ### Materials to fetch X-ray lines:

# - Al
# - As
# - C
# - Cu
# - Fe
# - Ga
# - Mo
# - O
# - Si

# imports
import hyperspy.api as hs


def get_the_lines_from_hspy():
    """Function to be exported. Getting only the specified lines from hspy
    Return: dict
    """

    Al = hs.material.elements.Al.Atomic_properties.Xray_lines.as_dictionary()
    As = hs.material.elements.As.Atomic_properties.Xray_lines.as_dictionary()
    C = hs.material.elements.C.Atomic_properties.Xray_lines.as_dictionary()
    Cu = hs.material.elements.Cu.Atomic_properties.Xray_lines.as_dictionary()
    Fe = hs.material.elements.Fe.Atomic_properties.Xray_lines.as_dictionary()
    Ga = hs.material.elements.Ga.Atomic_properties.Xray_lines.as_dictionary()
    Mo = hs.material.elements.Mo.Atomic_properties.Xray_lines.as_dictionary()
    O = hs.material.elements.O.Atomic_properties.Xray_lines.as_dictionary()
    Si = hs.material.elements.Si.Atomic_properties.Xray_lines.as_dictionary()

    lines_dict = {
        "Al": Al,
        "As": As,
        "C": C,
        "Cu": Cu,
        "Fe": Fe,
        "Ga": Ga,
        "Mo": Mo,
        "O": O,
        "Si": Si,
    }

    return lines_dict


def get_spesific_lines_from_hspy(lines_list):
    # Getting spesific lines from hspy
    lines_dict = {}
    for line in lines_list:
        try:
            element_info = hs.material.elements[line].Atomic_properties.Xray_lines.as_dictionary()
            lines_dict[line] = element_info
        except:
            print(f"Element '{line}' not found")
            continue
    
    return lines_dict

# everything above this line runs on import,
# while everything below this line only runs when this file is called directly
if __name__ == "__main__":
    # could have a test
    print(
        "function 'get_the_lines_from_hspy' is now avaliable.\n"
    )  # this does not run currently (12.09.22)
