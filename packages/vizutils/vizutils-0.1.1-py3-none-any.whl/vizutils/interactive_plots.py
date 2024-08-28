# vizutils/interactive_plots.py

import plotly.express as px
import pandas as pd

def interactive_scatter(data: pd.DataFrame, x: str, y: str, color: str = None, title: str = ""):
    """
    Create an interactive scatter plot.
    """
    fig = px.scatter(data, x=x, y=y, color=color, title=title)
    fig.show()

def interactive_line(data: pd.DataFrame, x: str, y: str, color: str = None, title: str = ""):
    """
    Create an interactive line plot.
    """
    fig = px.line(data, x=x, y=y, color=color, title=title)
    fig.show()

def interactive_histogram(data: pd.Series, nbins: int = 10, title: str = ""):
    """
    Create an interactive histogram.
    """
    fig = px.histogram(data, nbins=nbins, title=title)
    fig.show()
