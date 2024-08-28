# VizUtils

**VizUtils** is a Python library that simplifies the creation of various types of visualizations, ranging from basic plots to advanced and interactive visualizations. Whether you're performing exploratory data analysis or presenting insights, VizUtils provides an easy-to-use interface for generating insightful plots.

## Features

- **Basic Plots**: Create common visualizations like bar plots, histograms, line plots, and scatter plots with minimal code.

Below are examples of how to use different features of VizUtils.

from vizutils.basic_plots import bar_plot, histogram, line_plot, scatter_plot
import pandas as pd

# Load your dataset
df = pd.read_csv("data.csv")

# Bar Plot
bar_plot(df, x='category', y='values', title='Category vs Values')

# Histogram
histogram(df['values'], bins=15, title='Value Distribution')

# Line Plot
line_plot(df, x='date', y='values', title='Values Over Time')

# Scatter Plot
scatter_plot(df, x='feature1', y='feature2', title='Feature1 vs Feature2', hue='category')



- **Advanced Plots**: Generate more complex visualizations such as correlation heatmaps, pair plots, and box plots.

Below is the code example

from vizutils.advanced_plots import correlation_heatmap, pair_plot, box_plot

# Correlation Heatmap
correlation_heatmap(df, title='Correlation Matrix')

# Pair Plot
pair_plot(df, hue='category', title='Pair Plot of Features')

# Box Plot
box_plot(df, x='category', y='values', title='Box Plot of Values by Category')

- **Interactive Plots**: Use `Plotly` to create interactive plots that can be embedded in notebooks and web pages.

Below is the code example:

from vizutils.interactive_plots import interactive_scatter, interactive_line, interactive_histogram

# Interactive Scatter Plot
interactive_scatter(df, x='feature1', y='feature2', color='category', title='Interactive Scatter Plot')

# Interactive Line Plot
interactive_line(df, x='date', y='values', color='category', title='Interactive Line Plot')

# Interactive Histogram
interactive_histogram(df['values'], nbins=20, title='Interactive Histogram')

## Requirements
Python 3.6+
pandas
matplotlib
seaborn
plotly


## Installation

You can install VizUtils using `pip`:

```bash
pip install vizutils


