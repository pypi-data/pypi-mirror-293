from collections import OrderedDict
from typing import List

import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
from dateutil import tz
from dpd_lib.models import InfluxRecord

np.random.seed(1)


def plot_spectrogram(station: str, records: List[InfluxRecord]):
    # TODO

    x = [
        (record.timestamp).astimezone(tz.gettz("US/Pacific"))
        for record in records
    ]
    y = list(set([key for record in records for key in record.field_keys]))

    yzDict = OrderedDict[float, List]({y: [] for y in y})

    for record in records:
        for i in range(len(record.field_keys)):
            yzDict[record.field_keys[i]].append(record.field_values[i])

    fig = go.Figure(
        data=go.Heatmap(
            z=list(yzDict.values()),
            x=x,
            y=list(yzDict.keys()),
            colorscale="Viridis",
        )
    )

    fig.update_layout(title=f"{station} Spectrogram")

    # fig.show()

    # convert graph to JSON
    # fig_json = fig.to_json()

    # convert graph to PNG and encode it
    # png = pio.to_image(fig)
    # png_base64 = b64encode(png).decode("ascii")

    # convert graph to html
    fig = pio.to_html(fig, full_html=True)

    return fig
