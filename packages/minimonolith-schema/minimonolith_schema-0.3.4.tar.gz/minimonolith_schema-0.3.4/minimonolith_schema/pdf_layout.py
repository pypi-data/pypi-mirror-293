import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.backends.backend_pdf import PdfPages

def create_layout(filename, rows=3, cols=2):
  fig = plt.figure(figsize=(20, 30))  # Adjust size here.
  gs = GridSpec(2 * rows, 2 * cols, figure=fig)

  # This will merge every 2x2 grid into a larger subplot.
  merged_axes = np.array([[fig.add_subplot(gs[i:i+2, j:j+2]) for j in range(0, 2*cols, 2)] for i in range(0, 2*rows, 2)]).flatten()

  return {
    'pdf': PdfPages(filename),
    'rows': rows,
    'cols': cols,
    'current_index': 0,
    'fig': fig,
    'axes': merged_axes,
  }

def next_subplot(layout):
  if layout["current_index"] >= layout["rows"] * layout["cols"]:
    # Save the current figure before creating a new one.
    layout["pdf"].savefig(layout["fig"], bbox_inches='tight')
    # Create a new figure.
    layout = new_figure(layout)
  ax = layout["axes"][layout["current_index"]]
  layout["current_index"] += 1
  return ax, layout

def new_figure(layout):
  fig, axs = plt.subplots(layout["rows"], layout["cols"], figsize=(10, 30))  # Adjust size here.
  axs = axs.flatten()  # Important for the 1-D indexing
  layout["fig"] = fig
  layout["axes"] = axs
  layout["current_index"] = 0
  return layout

def save_figure(layout):
  if layout["fig"] is not None:
    layout["fig"].tight_layout()
    layout["pdf"].savefig(layout["fig"])
    layout["current_index"] = 0  # Reset index after saving
  layout["fig"], layout["axes"] = None, None
  return layout

def close_layout(layout):
  layout['pdf'].savefig(layout['fig'])  # Save the last page
  plt.close(layout['fig'])  # Close the last page
  layout['pdf'].close()  # Write the PDF file to disk
