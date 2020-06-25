import pandas as pd
import numpy as np
from bokeh.plotting import figure
from bokeh.models import HoverTool,ColumnDataSource, CategoricalColorMapper
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


def get_visual_df(vectors, df):
    """
    get the 2D-vector representation of text with original datafram
    and return a dataframe to be visualized
    :param vectors: 2D representation of text data
    :param df: a dataframe
    :return: new dataframe 
    """
    visual_df = pd.DataFrame(vectors, columns=(
        "x", "y"), index=df.index).join(df[["reviews", "labels"]])
    visual_df["description"] = ["Dissatisfied" if label==0 else "Disengaged" if label==1 else "Stoked" for label in visual_df["labels"]]
    visual_df["labels"] = visual_df["labels"].astype(str)
    return visual_df
    

def get_interactive_vec_plot(visual_df):
    """
    to visualize text data for better access and exploration
    :param visual_df: pandas dataframe
    :return: bokeh plot instance
    """

    datasource = ColumnDataSource(visual_df)

    colour_mapper = CategoricalColorMapper(factors=["0", "1", "2"], palette=["red", "purple", "green"])

    TOOLTIPS = [
        ("id", "@index"),
        ("text", "@reviews"),
        ("label", "@labels")
    ]

    hover = HoverTool(tooltips=TOOLTIPS)
    hover.attachment = 'right'

    plot = figure(
        title='2D-Vector Representation of Reviews',
        plot_width=600,
        plot_height=400,
        tools=('pan, wheel_zoom, reset', 'box_zoom', 'undo')
    )

    plot.add_tools(hover)

    plot.circle(
        'x', 
        'y', 
        source=datasource, 
        color=dict(field="labels", transform=colour_mapper), 
        legend="legend"
    )

    return plot


def get_vec_plot(visual_df):
    """
    to visualize text data investigating if labels are 
    clustered/seprated enough benefitial to model
    :param visual_df: a pandas dataframe
    :return: print out a pyplot instance
    """

    fig = plt.figure(figsize=(14, 10))

    colour_mapper = {"0": "red", "1": "purple", "2": "green"}

    plt.scatter(
        visual_df["x"],
        visual_df["y"],
        s=20,
        c=[colour_mapper[c] for c in visual_df["labels"]] 
    )

    handles = [Line2D([0], [0], marker="o", lw=0, markersize=8, color=c) for c in ["red", "purple", "green"]]
    labels = ["Dissatisfied", "Disengaged", "Stoked"]
    plt.legend(handles, labels)

    plt.title("2D-Vector Representation of Reviews")
    plt.gca().set_aspect("equal", "box")