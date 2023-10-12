import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import Dash, Input, Output, State, callback, dcc, html, dash_table
from dash_iconify import DashIconify
from utils.variables import SRC_PATH
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

location_data_path = SRC_PATH / "app_utils" / "assets" / "data" / "location.csv"
temp_data_path = SRC_PATH / "app_utils" / \
    "assets" / "data" / "temp_location.csv"

# if 'df' in globals():
#     pass
# else:
#     df = pd.read_csv(location_data_path)

# fig = go.Figure()


def generate_plotly_figure(df: pd.DataFrame) -> go.Figure:

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
            reversescale=True,
        ),
        name='Known Plume'
    )

    trace_x = go.Scattergeo(
        lon=df.loc[~df['detected'], 'lon'],
        lat=df.loc[~df['detected'], 'lat'],
        text=df.loc[~df['detected'], 'probability'],
        mode='markers',
        marker=dict(
            color=df['probability'],
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
        title='Customized GeoScatter Plot with Legend for Symbols',
        legend=dict(
            x=0.6,  # Adjust the x position of the legend
            y=0.2,  # Adjust the y position of the legend
            traceorder='normal',
        )
    )
    return fig


# fig.add_trace(go.Scattergeo(
#     lon=df['lon'],
#     lat=df['lat'],
#     text=df['probability'],
#     mode='markers',
#     marker=dict(
#         color=df['probability'],
#         colorscale='aggrnyl',
#         opacity=0.5,
#         cmin=0.5,
#         cmax=1,
#         colorbar=dict(title='Probability'),
#         size=7,
#         reversescale=True,
#         symbol=["circle" if detected else "square" for detected in df["detected"]],

#         )
#     ))


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
