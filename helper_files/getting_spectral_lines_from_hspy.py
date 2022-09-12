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
    """Getting only the specified lines from hspy
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


# this line will prevent the script to run on import of the file, and only run when called
# might be unnecessary here
if __name__ == "__main__":
    get_the_lines_from_hspy()
    print("you got the lines")
