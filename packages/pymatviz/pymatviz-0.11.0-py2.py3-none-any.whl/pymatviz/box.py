"""Bar plots."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import plotly.graph_objects as go


if TYPE_CHECKING:
    from collections.abc import Sequence

    import pandas as pd


def box_plot(
    df_in: pd.DataFrame, *, cols: Sequence[str] = (), **kwargs: Any
) -> go.Figure:
    """Plot a histogram of spacegroups shaded by crystal system.

    Args:
        df_in
        kwargs: Keywords passed to fig.add_box().

    Returns:
        go.Figure: plotly Figure depending on backend.
    """
    if cols == ():
        cols = df_in.select_dtypes("number")

    fig = go.Figure()
    # fig.layout.margin = dict(l=0, r=0, b=0, t=0)

    for idx, model in enumerate(cols):
        ys = [df_in[model].quantile(quant) for quant in (0.05, 0.25, 0.5, 0.75, 0.95)]

        fig.add_box(y=ys, name=model, width=0.7, **kwargs)

        # Add an annotation for the interquartile range
        IQR = ys[3] - ys[1]
        median = ys[2]
        fig.add_annotation(
            x=idx, y=1, text=f"{IQR:.2}", showarrow=False, yref="paper", yshift=-10
        )
        fig.add_annotation(
            x=idx,
            y=median,
            text=f"{median:.2}",
            showarrow=False,
            yshift=7,
            # bgcolor="rgba(0, 0, 0, 0.2)",
            # width=50,
        )
    fig.add_annotation(
        x=-0.6, y=1, text="IQR", showarrow=False, yref="paper", yshift=-10
    )

    fig.layout.legend.update(orientation="h", y=1.2)
    # prevent x-labels from rotating
    fig.layout.xaxis.tickangle = 0
    # use line breaks to offset every other x-label
    x_labels_with_offset = [
        f"{'<br>' * (idx % 2)}{label}" for idx, label in enumerate(cols)
    ]
    fig.layout.xaxis.update(tickvals=cols, ticktext=x_labels_with_offset)
    return fig
