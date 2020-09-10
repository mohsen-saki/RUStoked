import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from PIL import Image

import sys
sys.path.append("..")
from pathlib import Path


def get_barchart(fields, values, titles=None, legends=None):
    """
    plot a bar horizontal chart
    :param fields: list-like fields or variables to be visualized
    :param velues: list-of-list-like amounts for each fieald (bars are horizontally stacked)
    :param titles: list of title and lables to be ploted on the chart
                    thier order matters -> [title, xlabel, ylabel]
    :param legends: list of legends names to be ploted on the chart
    :return: plot a bar chart
    """
    # keep track of charts created
    legend_handeler = []
    # handeling the stacked bar chart
    stack = values.copy()
    stack.insert(0, np.zeros(len(values[0])))
    stack = np.cumsum(stack, axis=0)
    colors = ['teal', 'goldenrod', 'darkviolet']

    # create an instance of canvas and axes
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot()
    
    # craet bar chart(s)
    for i in range(len(values)):
        chart = ax.barh(fields, values[i], left=stack[i], height=0.5, color=colors[i])
        legend_handeler.append(chart[0])
        
    # set plot title & axis labels if given
    if titles:
        ax.set_title(titles[0])
        ax.set_xlabel(titles[1])
        ax.set_ylabel(titles[2])

    # add legend if given
    if legends:
        ax.legend(legend_handeler, legends, bbox_to_anchor=(1.05, 1.0), loc='upper left')
    
    plt.show()



def get_word_cloud(text, title="", mask_path=None):
    """
    creat a word cloud visual from given text
    :param text: text (string) data to be visualized
    :param mask_path: a path to the image to be used as a template for word cloud
    :return: plot a word cloud
    """
    if mask_path:
        mask = np.array(Image.open(mask_path))
    else:
        mask=None
        
    wc = WordCloud(
        background_color='black',
        collocations=True,
        colormap='autumn',
        max_font_size=30,
        mask=mask
    )
    
    wc.generate(text)

    fig = plt.figure(figsize=(12, 8))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.title(title)
    plt.show()