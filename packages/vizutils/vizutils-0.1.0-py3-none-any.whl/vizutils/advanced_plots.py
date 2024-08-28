# vizutils/advanced_plots.py

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def correlation_heatmap(data: pd.DataFrame, title: str = ""):
    """
    Create a correlation heatmap.
    """
    plt.figure(figsize=(12, 8))
    sns.heatmap(data.corr(), annot=True, cmap='coolwarm', fmt='.2f')
    plt.title(title)
    plt.show()

def pair_plot(data: pd.DataFrame, hue: str = None, title: str = ""):
    """
    Create a pair plot.
    """
    sns.pairplot(data, hue=hue)
    plt.suptitle(title)
    plt.show()

def box_plot(data: pd.DataFrame, x: str, y: str, title: str = ""):
    """
    Create a box plot.
    """
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=x, y=y, data=data)
    plt.title(title)
    plt.show()
