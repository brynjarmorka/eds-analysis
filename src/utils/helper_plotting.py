# Helper funcs for plotting


import matplotlib.pyplot as plt
import numpy as np
import hyperspy.api as hs
import plotly.graph_objects as go

from utils.get_raw_data import get_raw_data_array, locate_raw_data


def simple_hspy_plot(filenr, start=0.0, stop=20.0, elements=None, xray_lines=True):
    """
    Plot a simple hspy plot with hspy methods.
    """
    # # if elements is a string, convert to list # did not work
    # if (type(elements) == str) and ((len(elements == 1)) or len(elements) == 2):
    #     elements = [elements]
    emsa_paths = locate_raw_data()
    s = hs.load(emsa_paths[filenr], signal_type="EDS_SEM")
    # s.set_signal_type("EDS_SEM")
    if elements:
        s.add_elements(elements)
    s.isig[start:stop].plot(xray_lines=xray_lines)
    # print(s.metadata)


def simple_matplotlib_plot(filenr, start=0, stop=2048):
    """
    Plot a simple matplotlib plot of the raw data.
    """
    fig, axs = plt.subplots(nrows=1, ncols=1, figsize=(6, 6), tight_layout=True)
    y = get_raw_data_array(filenr, normalize=True)
    #
    x = np.arange(0, 2048, 1)  # making the 2048 long x-axis as channel numbers
    axs.set_title(
        "X-ray intensities normalized to 1 for the highets peak in the spectrum"
    )
    axs.set_xlabel("channel number (~10eV)")
    # start = linmap_kev_to_index(start)
    # stop = linmap_kev_to_index(stop)
    axs.step(x[start:stop], y[start:stop])


def simple_plot_with_lines(filenr, lines, kev=False, start=0, stop=2048):
    """
    Matplotlib plot with lines at channel number

    """
    fig, axs = plt.subplots(nrows=1, ncols=1, figsize=(6, 6), tight_layout=True)
    y = get_raw_data_array(filenr, normalize=True)
    #
    x = np.arange(0, 2048, 1)  # making the 2048 long x-axis as channel numbers
    axs.set_title(
        "X-ray intensities normalized to 1 for the highets peak in the spectrum"
    )
    axs.set_xlabel("channel number (~10eV)")
    # start = linmap_kev_to_index(start)
    # stop = linmap_kev_to_index(stop)
    axs.step(x[start:stop], y[start:stop])
    for line in lines:
        if (line > start) and (line < stop):
            axs.axvline(line, color="red", linestyle="--")


# simple_plot_with_lines(10, [250, 1760], start=225, stop=350)


def plot_multiple_spectra(arrays, start=0, stop=2048, split=None):
    """
    Plot multiple data arrays from the raw data using matplotlib.
    """
    fig, axs = plt.subplots(nrows=1, ncols=1, figsize=(15, 3), tight_layout=True)
    x = np.arange(0, 2048, 1)  # making the 2048 long x-axis as channel numbers
    for i in range(len(arrays)):
        if split:
            axs.step(
                x[start:stop],
                arrays[i][1][start:stop] + i * split,
                label=f"{arrays[i][0]} + {i*split:.2f}",
            )
        else:
            axs.step(x[start:stop], arrays[i][1][start:stop], label=arrays[i][0])
    axs.set_title(
        "X-ray intensities normalized to 1 for the highets peak in one spectrum"
    )
    axs.set_xlabel("channel number (~10eV)")
    axs.legend()


def plotly_plot_multiple_spectra(
    arrays, start=0, stop=2048, split=None, show=False, mode="lines+markers", x=None
):
    """
    Using plotly to make an interactive plot with mulitple arrays.

    Use split to split the lines.

    Returns a plotly figure object.
    """
    if x is None:
        x = np.arange(0, 2048, 1)  # making the 2048 long x-axis as channel numbers
    fig = go.Figure()
    for i in range(len(arrays)):
        if split:
            fig.add_trace(
                go.Scatter(
                    x=x[start:stop],
                    y=arrays[i][1][start:stop] + i * split,
                    mode=mode,
                    name=f"{arrays[i][0]} + {i*split:.2f}",
                )
            )
        else:
            fig.add_trace(
                go.Scatter(
                    x=x[start:stop],
                    y=arrays[i][1][start:stop],
                    mode=mode,
                    name=arrays[i][0],
                )
            )
    fig.update_layout(
        title="Spectroscopy lines",
        xaxis_title="Channel number [~10eV]",
        yaxis_title="Relative intensity [a.u.]",
        legend_title="Files used",
    )
    if show:
        fig.show()
    return fig


def plotly_simple(
    x_arrs,
    y_arrs,
    title="Title",
    xaxis_title="Channel number [~10eV]",
    yaxis_title="Relative intensity [a.u.]",
    mode="lines+markers",
    names=None,
    show=False,
):
    """
    Plot a simple plotly plot.
    """
    if names is None:
        names = np.arange(0, len(x_arrs), 1)
    fig = go.Figure()
    for i in range(len(x_arrs)):
        fig.add_trace(
            go.Scatter(
                x=x_arrs[i],
                y=y_arrs[i],
                mode=mode,
                name=names[i],
            )
        )
    fig.update_layout(
        title=title,
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
    )
    if show:
        fig.show()
    return fig
