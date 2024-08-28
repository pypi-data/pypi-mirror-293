# vizutils/basic_plots.py

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def bar_plot(data: pd.DataFrame, x: str, y: str, title: str = ""):
    """
    Create a bar plot.
    """
    plt.figure(figsize=(10, 6))
    sns.barplot(x=x, y=y, data=data)
    plt.title(title)
    plt.show()

def histogram(data: pd.Series, bins: int = 10, title: str = ""):
    """
    Create a histogram.
    """
    plt.figure(figsize=(10, 6))
    sns.histplot(data, bins=bins)
    plt.title(title)
    plt.show()

def line_plot(data: pd.DataFrame, x: str, y: str, title: str = ""):
    """
    Create a line plot.
    """
    plt.figure(figsize=(10, 6))
    sns.lineplot(x=x, y=y, data=data)
    plt.title(title)
    plt.show()

def scatter_plot(data: pd.DataFrame, x: str, y: str, title: str = "", hue: str = None):
    """
    Create a scatter plot.
    """
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=x, y=y, hue=hue, data=data)
    plt.title(title)
    plt.show()
