import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import colorConverter
import seaborn as sns


WEEK = "MTWRF"

def plot_grid(figsize=(16, 10)):
    """
    Creates a matplotlib figure and plots on it a weekly time grid.

    figsize:
        A tuple with the dimensions of the figure.

    Returns:
        A tuple consisting of the matplotlib figure and the axes
        object with the plot of the grid.
    """

    sns.set_style("whitegrid")
    fig = plt.figure(figsize=figsize)
    ax = plt.gca()

    ax.set_xlim(0, 5)
    ax.set_ylim(8, 19)
    ax.set_xticks(range(5))
    ax.set_xticklabels('')
    ax.set_xticks(np.arange(5) + 0.5, list(WEEK), minor=True)
    ax.set_yticks(range(8, 19, 1))
    ax.tick_params(axis='y', which='major', labelsize=24)
    ax.tick_params(axis='x', which='minor', labelsize=24)
    ax.set_axisbelow(True)
    ax.invert_yaxis()
    return fig, ax



def plot_rect(ax, x, y, w=1, h=1, color ='coral', alpha=0.3, text="", fontsize=12):
    """
    Utility function adding rectangles to a class schedule.

    ax:
        Matplotlib axes object to add the rectangle to.
    x, y:
        Coordinates of the lower left corner of the rectangle.
    w, h:
        Width and height of the rectangle.
    color:
        Color of the patch.
    alpha:
        Transparency of the face color.
    text:
        Label printed in the center of the rectangle.
    fontsize:
        Label font size.
    """

    rectangle = patches.Rectangle(
                             (x, y),
                             width = w,
                             height = h,
                             edgecolor = colorConverter.to_rgba(color, 1),
                             facecolor = colorConverter.to_rgba(color, alpha),
                             linewidth = 1
                            )

    rx, ry = rectangle.get_xy()
    cx = rx + rectangle.get_width()/2.0
    cy = ry + rectangle.get_height()/2.0
    ax.add_patch(rectangle)
    ax.annotate(text, (cx, cy),
                color='k',
                fontsize=fontsize,
                weight='bold',
                ha='center',
                va='center')



def plot_schedule(df):
    """
    Plots a schedule of classes.

    df:
        Dataframe with class schedule information -
        one class per row.

    Returns:
        Matplotlib figure with the plot.
    """


    fig, ax = plot_grid()

    df = df.copy()

    df = df[df["start"].notna()]
    df = df[df["end"].notna()]
    df = df[df["days"].notna()]
    df = df.reset_index(drop=True)

    et = pd.to_datetime(df["end"], format="%I:%M%p", errors="coerce")
    st =  pd.to_datetime(df["start"], format="%I:%M%p", errors="coerce")
    et = et.dt.hour + et.dt.minute/60
    st = st.dt.hour + st.dt.minute/60
    df["st"] = st
    df["duration"] = et - st
    df = df[df["duration"].notna()]
    if len(df) == 0:
        return fig

    for i in df.index:
        r = df.loc[i]
        for x, day in enumerate(WEEK):
            if day not in r["days"]:
                continue
            y = r["st"]
            h = r["duration"]
            course = r["course_num"]
            faculty = r["faculty"]
            room = r["room"]
            text = f'{course}\n{faculty}\n{room}'
            if r["type"] == "LEC":
                color = 'red'
            elif r["type"] == "REC":
                color = "orange"
            else:
                color = "limegreen"
            plot_rect(ax, x, y, w=1, h=h, color=color, text=text)

    return fig
