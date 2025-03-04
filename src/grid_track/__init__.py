from pathlib import Path
import dash
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px


class GridProgress:
    def __init__(self, csv_path: Path):
        self.csv_path = csv_path
        self.app = dash.Dash(
            __name__,
            external_stylesheets=[dbc.themes.BOOTSTRAP],
            suppress_callback_exceptions=True,
        )
        self.app.layout = dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [dcc.Graph(id="grid-progress")],
                            width=4,
                            style={"padding": "2px"},
                        ),
                        dbc.Col(
                            [dcc.Graph(id="text")],
                            width=4,
                            style={"padding": "2px"},
                        ),
                        dbc.Col(
                            [
                                dcc.Graph(
                                    id="Elevation",
                                    style={
                                        "padding": "2px",
                                        "margin": "0px",
                                    },
                                ),
                            ],
                            width=4,
                            style={"padding": "2px"},
                        ),
                    ],
                    style={"margin": "0px"},
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [dcc.Graph(id="cuts")],
                            width=4,
                            style={"padding": "2px"},
                        ),
                        dbc.Col(
                            [dcc.Graph(id="heatmap")],
                            width=4,
                            style={"padding": "2px"},
                        ),
                        dbc.Col(
                            [dcc.Graph(id="Time")],
                            width=4,
                            style={"padding": "2px"},
                        ),
                    ],
                    style={"margin": "0px"},
                ),
                dcc.Interval(id="interval-component", interval=250, n_intervals=0),
            ],
            fluid=True,
            style={"padding": "0px"},
        )

        self.app.callback(
            [
                Output("grid-progress", "figure"),
                Output("text", "figure"),
                Output("cuts", "figure"),
                Output("heatmap", "figure"),
                Output("Elevation", "figure"),  # Add Output for Elevation
            ],
            [Input("interval-component", "n_intervals")],
        )(self.update_graphs)

    def update_graphs(self, n):
        df = pd.read_csv(self.csv_path)

        # Grid progress plot
        fig_grid = px.line(
            df, x="azimuth", y="elevation", title="Grid progress", line_shape="linear"
        )
        fig_grid.add_scatter(
            x=df["azimuth"],
            y=df["elevation"],
            mode="markers",
            marker=dict(color="blue"),
        )
        fig_grid.update_traces(showlegend=False)  # Remove the "trace 1" output text
        fig_grid.update_layout(
            margin=dict(l=0, r=0, t=60, b=0),
            xaxis=dict(dtick=15),
            yaxis=dict(dtick=15),
            title=dict(x=0.5, xanchor="center", font=dict(size=18)),
        )

        # Text plot
        fig_text = px.scatter(df, x="timestamp", y="amplitude", title="Text")
        fig_text.update_layout(
            margin=dict(l=0, r=0, t=60, b=0),
            title=dict(x=0.5, xanchor="center", font=dict(size=18)),
        )

        # Cuts (azimuth)
        df_cut_0 = df[df["cut_index"] == 0]
        fig_cuts = px.line(df_cut_0, x="azimuth", y="amplitude", title="Cuts (azimuth)")
        fig_cuts.update_layout(
            margin=dict(l=0, r=0, t=60, b=0),
            xaxis=dict(dtick=15),
            title=dict(x=0.5, xanchor="center", font=dict(size=18)),
        )
        fig_cuts.data = []  # Clear the initial data
        cut_indexes = df["cut_index"].unique()
        highest_cut_index = max(cut_indexes)
        for cut_index in cut_indexes:
            df_cut = df[df["cut_index"] == cut_index]
            line = dict(color="gray", width=0.25)
            if cut_index == highest_cut_index:
                line = dict(color="blue", width=3)
            fig_cuts.add_scatter(
                x=df_cut["azimuth"],
                y=df_cut["amplitude"],
                mode="lines",
                line=line,
                showlegend=False,  # Disable labels
            )

        # Heatmap plot
        fig_heatmap = px.density_heatmap(
            df,
            x="azimuth",
            y="elevation",
            z="amplitude",
            title="Heatmap",
            histfunc="avg",
            nbinsx=20,
            nbinsy=20,
            color_continuous_scale="RdBu_r",
        )
        fig_heatmap.update_layout(
            margin=dict(l=0, r=0, t=60, b=0),
            xaxis_showgrid=True,
            yaxis_showgrid=True,
            xaxis_layer="above traces",
            yaxis_layer="above traces",
            xaxis=dict(dtick=15),
            yaxis=dict(dtick=15),
            coloraxis_colorbar=dict(title=None),  # Remove the text above the colorbar
            title=dict(x=0.5, xanchor="center", font=dict(size=18)),
        )

        # Elevation (similar to Cuts (azimuth))
        df_cut_0 = df[df["cut_index"] == 0]
        fig_elevation = px.line(df_cut_0, x="elevation", y="amplitude", title="Cuts (elevation)")
        fig_elevation.update_layout(
            margin=dict(l=0, r=0, t=60, b=0),
            xaxis=dict(dtick=15),
            title=dict(x=0.5, xanchor="center", font=dict(size=18)),
        )
        fig_elevation.data = []  # Clear the initial data
        cut_indexes = df["cut_index"].unique()
        highest_cut_index = max(cut_indexes)
        for cut_index in cut_indexes:
            df_cut = df[df["cut_index"] == cut_index]
            line = dict(color="gray", width=0.25)
            if cut_index == highest_cut_index:
                line = dict(color="blue", width=3)
            fig_elevation.add_scatter(
                x=df_cut["elevation"],
                y=df_cut["amplitude"],
                mode="lines",
                line=line,
                showlegend=False,  # Disable labels
            )

        return fig_grid, fig_text, fig_cuts, fig_heatmap, fig_elevation  # Add fig_elevation to return values

    def run(self, debug: bool | None = None, *args, **kwargs):
        self.app.run(
            debug=debug,
            *args,
            **kwargs,
        )


if __name__ == "__main__":
    grid_progress = GridProgress(csv_path=Path("data/fake_data.csv"))
    grid_progress.run(
        debug=True,
        # debug=False,    # Disable button on bottom right
    )
