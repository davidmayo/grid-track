from pathlib import Path
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px


class GridProgress:
    def __init__(self, csv_path: Path):
        self.csv_path = csv_path
        self.app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
        self.app.layout = dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                # html.H5("Grid progress", style={'textAlign': 'center'}),
                                dcc.Graph(id="grid-progress")
                            ],
                            width=6,
                        ),
                        dbc.Col(
                            [
                                # html.H5("Text", style={'textAlign': 'center'}),
                                dcc.Graph(id="text")
                            ],
                            width=6,
                        ),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                # html.H5("Cuts", style={'textAlign': 'center'}),
                                dcc.Graph(id="cuts")
                            ],
                            width=6,
                        ),
                        dbc.Col(
                            [
                                # html.H5("Heatmap", style={'textAlign': 'center'}),
                                dcc.Graph(id="heatmap")
                            ],
                            width=6,
                        ),
                    ]
                ),
                dcc.Interval(id="interval-component", interval=250, n_intervals=0),
            ],
            fluid=True,
        )

        self.app.callback(
            [
                Output("grid-progress", "figure"),
                Output("text", "figure"),
                Output("cuts", "figure"),
                Output("heatmap", "figure"),
            ],
            [Input("interval-component", "n_intervals")],
        )(self.update_graphs)

    def update_graphs(self, n):
        df = pd.read_csv(self.csv_path)

        # Grid progress plot
        fig_grid = px.line(df, x="timestamp", y="amplitude", title="Grid progress")

        # Text plot
        fig_text = px.scatter(df, x="timestamp", y="amplitude", title="Text")

        # Cuts (azimuth)
        df_cut_0 = df[df["cut_index"] == 0]
        fig_cuts = px.line(df_cut_0, x="azimuth", y="amplitude", title="Cuts (azimuth)")
        fig_cuts.data = []  # Clear the initial data
        cut_indexes = df["cut_index"].unique()
        highest_cut_index = max(cut_indexes)
        for cut_index in cut_indexes:
            df_cut = df[df["cut_index"] == cut_index]
            line = dict(color='gray', width=0.25)
            if cut_index == highest_cut_index:
                line = dict(color='blue', width=3)
            fig_cuts.add_scatter(
                x=df_cut["azimuth"],
                y=df_cut["amplitude"],
                mode='lines',
                line=line,
                showlegend=False  # Disable labels
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
            xaxis_showgrid=True,
            yaxis_showgrid=True,
            xaxis_layer="above traces",
            yaxis_layer="above traces",
            xaxis=dict(dtick=15),
            yaxis=dict(dtick=15),
        )

        return fig_grid, fig_text, fig_cuts, fig_heatmap

    def run(self):
        self.app.run_server(
            debug=True,
        )


if __name__ == "__main__":
    grid_progress = GridProgress(csv_path=Path("data/fake_data.csv"))
    grid_progress.run()
