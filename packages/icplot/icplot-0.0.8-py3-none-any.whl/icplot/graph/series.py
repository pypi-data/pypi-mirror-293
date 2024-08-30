import json


class PlotSeries:

    def __init__(self, label: str = ""):
        self.label = label
        self.color: list[float] = [0.0, 0.0, 0.0]
        self.series_type = ""

    def serialize(self):
        return {"label": self.label, "color": self.color, "type": self.series_type}

    def __str__(self):
        return json.dumps(self.serialize(), indent=4)


class ImageSeries(PlotSeries):
    def __init__(self, data, label: str = "", transform=None):
        super().__init__(label)
        self.data = data
        self.series_type = "image"
        self.transform = transform

    def serialize(self):
        ret = super().serialize()
        ret["data"] = self.data
        return ret


class LinePlotSeries(PlotSeries):
    def __init__(self, x: list[float], y: list[float], label: str = "") -> None:
        super().__init__(label)
        self.series_type = "line"
        self.x = x
        self.y = y

    def serialize(self):
        ret = super().serialize()
        ret["x"] = self.x
        ret["y"] = self.y
        return ret


class ScatterPlotSeries(PlotSeries):
    def __init__(self, data, label: str = ""):
        super().__init__(label)
        self.data = data
        self.series_type = "scatter"

    def serialize(self):
        ret = super().serialize()
        ret["data"] = self.data
        return ret
