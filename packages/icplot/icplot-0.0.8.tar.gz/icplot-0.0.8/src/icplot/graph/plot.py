"""
This module has content for generating plots
"""

import random
from pathlib import Path
from typing import cast
import json

from .series import PlotSeries, LinePlotSeries, ScatterPlotSeries, ImageSeries
from .matplotlib_plot_backend import MatplotlibPlotBackend, MatplotlibColorMap


class Range:

    def __init__(self, lower, upper, step):
        self.lower = lower
        self.upper = upper
        self.step = step

    def eval(self):
        return range(self.lower, self.upper, self.step)

    def serialize(self):
        return {"lower": self.lower, "upper": self.upper, "step": self.step}

    def __str__(self):
        return json.dumps(self.serialize(), ident=4)


class Plot:
    """
    A generic plot with optional axis ticks
    """

    def __init__(
        self,
        title: str = "",
        x_label: str = "",
        y_label: str = "",
        legend_label: str = "",
    ) -> None:
        self.series: list[PlotSeries] = []
        self.title = title
        self.size: tuple | None = None
        self.plot_type = ""
        self.x_label = x_label
        self.y_label = y_label
        self.legend_label = legend_label
        self.x_ticks: Range | None = None
        self.y_ticks: Range | None = None
        self.backend = MatplotlibPlotBackend()
        self.cmap = MatplotlibColorMap("viridis")

    def set_colour_map(self, cmap):
        self.c_map = MatplotlibColorMap(cmap)

    def set_x_ticks(self, lower, upper, step):
        self.x_ticks = Range(lower, upper + 1, step)

    def set_y_ticks(self, lower, upper, step):
        self.y_ticks = Range(lower, upper + 1, step)

    def set_decorations(self):

        xtick_range = None
        ytick_range = None
        if self.x_ticks:
            xtick_range = self.x_ticks.eval()
        if self.y_ticks:
            ytick_range = self.y_ticks.eval()

        self.backend.set_decorations(
            self.x_label,
            self.y_label,
            self.title,
            xtick_range,
            ytick_range,
        )

    def add_series(self, series):
        self.series.append(series)

    def plot_series(self, series, label):
        if series.series_type == "line":
            line_series = cast(LinePlotSeries, series)
            self.backend.plot_line(
                line_series.x, line_series.y, label=label, color=series.color
            )
        elif series.series_type == "scatter":
            scatter_series = cast(ScatterPlotSeries, series)
            self.backend.plot_scatter(
                scatter_series.data, label=label, color=series.color
            )
        elif series.series_type == "image":
            image_series = cast(ImageSeries, series)
            self.backend.plot_image(image_series.data)

    def plot(self, path: Path | None = None):
        for idx, series in enumerate(self.series):
            series.color = self.cmap.get_color(idx, self.series)

        first = True
        for series in self.series:
            label = series.label
            if first and self.legend_label:
                label = f"{label} {self.legend_label}"
                first = False
            self.plot_series(series, label)

        self.set_decorations()
        self.backend.render(path)

    def serialize(self):
        return {
            "series": [s.serialize() for s in self.series],
            "title": self.title,
            "type": self.plot_type,
            "xlabel": self.x_label,
            "ylabel": self.y_label,
            "legend_label": self.legend_label,
            "xticks": self.x_ticks.serialize(),
            "yticks": self.y_ticks.serialize(),
        }


class GridPlot(Plot):
    """
    Make a grid of plots
    """

    def __init__(
        self, title: str = "", stride: int = 4, size: tuple = (25, 20)
    ) -> None:
        super().__init__(title)
        self.stride = stride
        self.size = size

    def _subplot(self, rows: int, cols: int, count: int, series):

        self.backend.make_subplot(rows, cols, count)
        self.plot_series(series, "")
        return count + 1

    def render(self, data, path: Path, num_samples: int = 0):
        rows = num_samples // self.stride
        cols = num_samples // rows
        count = 1
        if num_samples == 0:
            indices = [random.randint(0, len(data) - 1) for _ in range(num_samples)]
        else:
            indices = list(range(0, len(data)))

        for index in indices:
            if num_samples > 0 and count == num_samples + 1:
                break
            if isinstance(data[index], list):
                for series in data[index]:
                    count = self._subplot(rows, cols, count, series)
            else:
                count = self._subplot(rows, cols, count, data[index])

        self.backend.render(path)
