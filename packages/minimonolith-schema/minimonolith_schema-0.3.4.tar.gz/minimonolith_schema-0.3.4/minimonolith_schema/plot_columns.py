import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

import pdf_layout

def plot_string_category(data, column, layout):
  ax, layout = pdf_layout.next_subplot(layout)
  value_counts = data[column].value_counts().head(10)  # Top 10 categories
  ax.bar(x=value_counts.index, height=value_counts.values)
  ax.set_title(f'Barplot of {column}')
  ax.tick_params(axis='x', rotation=90)
  caption = f'There are {data[column].nunique()} unique values. Most frequent: {value_counts.index[0]}'
  ax.text(0.5, -0.2, caption, size=12, ha="center",
          transform=ax.transAxes)
  return layout

def plot_integer_category(data, column, layout):
  ax, layout = pdf_layout.next_subplot(layout)
  ax.hist(data[column], bins=30)
  ax.set_title(f'Histogram of {column}')
  ax.tick_params(axis='x', rotation=90)
  caption = f'There are {data[column].nunique()} unique values. Most frequent: {data[column].mode()[0]}'
  ax.text(0.5, -0.2, caption, size=12, ha="center",
          transform=ax.transAxes)
  return layout

def plot_float_distribution(data, column, layout):
  ax, layout = pdf_layout.next_subplot(layout)
  ax.boxplot(data[column])
  ax.set_title(f'Boxplot of {column}')
  ax.tick_params(axis='x', rotation=90)
  mean = data[column].mean()
  median = data[column].median()
  std_dev = data[column].std()
  caption = f'Mean: {mean:.2f}, Median: {median:.2f}, Std. Dev.: {std_dev:.2f}'
  ax.text(0.5, -0.2, caption, size=12, ha="center",
          transform=ax.transAxes)
  return layout

def plot_string_individuals(data, column, layout):
  ax, layout = pdf_layout.next_subplot(layout)
  ax.hist(data[column].str.len(), bins=30)
  ax.set_title(f'Histogram of String Lengths in {column}')
  ax.tick_params(axis='x', rotation=90)
  mean_len = data[column].str.len().mean()
  mode_len = data[column].str.len().mode()[0]
  caption = f'Average length: {mean_len:.2f}, Most common length: {mode_len}'
  ax.text(0.5, -0.2, caption, size=12, ha="center",
          transform=ax.transAxes)
  return layout

"""
# For plotting categorical strings
def plot_string_category(data, column):
    plt.figure(figsize=(10,6))
    value_counts = data[column].value_counts().head(10)  # Top 10 categories
    sns.barplot(x=value_counts.index, y=value_counts.values)
    plt.title(f'Barplot of {column}')
    plt.xticks(rotation=90)
    plt.show()

# For plotting categorical integers
def plot_integer_category(data, column, bins=30):
    plt.figure(figsize=(10,6))
    sns.histplot(data[column], bins=bins, kde=True)
    plt.title(f'Histogram of {column}')
    plt.show()

# For plotting floating-point numbers (as distribution)
def plot_float_distribution(data, column):
    plt.figure(figsize=(10,6))
    sns.boxplot(x=data[column])
    plt.title(f'Boxplot of {column}')
    plt.show()

# For plotting individual string lengths
def plot_string_individuals(data, column):
    plt.figure(figsize=(10,6))
    sns.histplot(data[column].str.len(), bins=30, kde=True)
    plt.title(f'Histogram of String Lengths in {column}')
    plt.show()
"""

def plot_column(data, column, layout):
  ax, layout = pdf_layout.next_subplot(layout)
  if pd.api.types.is_numeric_dtype(data[column]):
    if data[column].nunique() < 30:  # If less than 30 unique values, consider it categorical
      plot_integer_category(data, column, layout)
    else:
      plot_float_distribution(data, column, layout)
  elif pd.api.types.is_string_dtype(data[column]):
    if data[column].nunique() < 30:  # If less than 30 unique values, consider it categorical
      plot_string_category(data, column, layout)
    else:
      plot_string_individuals(data, column, layout)
  ax.tick_params(axis='x', rotation=90)
  return layout

def plot_columns(df):
  pdfName='plots.pdf';
  layout = pdf_layout.create_layout(pdfName, rows=6, cols=2);
  for col in df.columns:
    plot_column(df, col, layout);
  pdf_layout.close_layout(layout);
