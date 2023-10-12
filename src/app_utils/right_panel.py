import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

import pandas as pd

import plotly.graph_objects as go

from dash_iconify import DashIconify

from utils.variables import SRC_PATH

location_data_path = SRC_PATH / "app_utils" / "assets" / "data" /\
    "location.csv"
temp_data_path = SRC_PATH / "app_utils" / \
    "assets" / "data" / "temp_location.csv"


def generate_plotly_figure(df: pd.DataFrame) -> go.Figure:
    """generate the geoscatter plot of the plumes

    Args:
        df (pd.DataFrame): dataframe containing the plume data

    Returns:
        go.Figure: plotly figure
    """

    trace_circle = go.Scattergeo(
        lon=df.loc[df['detected'], 'lon'],
        lat=df.loc[df['detected'], 'lat'],
        text=df.loc[df['detected'], 'probability'],
        mode='markers',
        marker=dict(
            color="red",
            symbol='square',
            opacity=0.6,
            size=7,
        ),
        name='Known Plume'
    )

    trace_x = go.Scattergeo(
        lon=df.loc[~df['detected'], 'lon'],
        lat=df.loc[~df['detected'], 'lat'],
        text=df.loc[~df['detected'], 'probability'],
        mode='markers',
        marker=dict(
            color=df.loc[~df['detected'], 'probability'],
            symbol="circle",
            colorscale='Plotly3',
            opacity=0.8,
            cmin=0.5,
            cmax=1,
            colorbar=dict(title='Probability'),
            size=7,
            reversescale=True),
        name='Plume Detected by the Model'
    )
    fig = go.Figure(data=[trace_circle, trace_x])

    fig.update_layout(
        legend=dict(
            x=0.6,  # Adjust the x position of the legend
            y=0.2,  # Adjust the y position of the legend
            traceorder='normal',
        )
    )
    return fig


def result():
    return dbc.Card([

        dmc.Tabs([
            dmc.TabsList([
                dmc.Tab(
                    "Image",
                    icon=DashIconify(icon="ri:image-line"),
                    value="image",
                ),
                dmc.Tab(
                    "Global Map of Plumes",
                    icon=DashIconify(icon="mingcute:earth-2-line"),
                    value="global_map",
                ),
            ]),
            dmc.TabsPanel(value="image", id="image_tab"),
            dmc.TabsPanel(value="image", id="model_result_tab"),
            dmc.TabsPanel(value="global_map", id="global_map_tab"),
        ],
            value="image",
        )
    ], id="results")


def right_panel():
    return dbc.Col([
        result()
    ], id="right_column")
