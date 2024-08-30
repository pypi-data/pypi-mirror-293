from pathlib import Path
import logging

logging.getLogger("matplotlib").setLevel(logging.WARNING)
import matplotlib  # NOQA

default_backend = matplotlib.get_backend()
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # NOQA
import matplotlib as mpl  # NOQA

from icplot.color import ColorMap  # NOQA


class MatplotlibColorMap(ColorMap):

    def __init__(self, label: str):
        super().__init__(label)
        self.c_map = mpl.colormaps[label]
        self.cmap_start_offset = 0.25
        self.cmap_scale = 2

    def get_color(self, cursor: int, values: list):
        """
        Returns a colour based on a cmap and how far across
        the datasets you are
        """
        position = cursor / len(values)
        return self.c_map(self.cmap_start_offset + (position / self.cmap_scale))


class MatplotlibPlotBackend:

    def __init__(self):
        self.ax = plt.subplot(111)

    def set_decorations(self, x_label, y_label, title, x_ticks, y_ticks):
        self.ax.legend(loc="upper left")
        if x_label:
            self.ax.set_xlabel(x_label)
        if y_label:
            self.ax.set_ylabel(y_label)
        if title:
            self.ax.set_title(title)
        if x_ticks:
            self.ax.set_xticks(x_ticks)
        if y_ticks:
            self.ax.set_yticks(y_ticks)

    def plot_line(self, x, y, label, color):
        self.ax.plot(x, y, label=label, color=color)

    def plot_scatter(self, data, label, color):
        self.ax.plot(data, label=label, color=color)

    def make_subplot(self, rows, cols, count):
        plt.subplot(rows, cols, count)

    def plot_image(self, data):
        plt.imshow(data)
        plt.axis("off")

    def render(self, path: Path | None = None):
        if path:
            plt.savefig(path)
        else:
            plt.switch_backend(default_backend)
            plt.show()
            plt.switch_backend("Agg")
