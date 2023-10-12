import base64
import datetime
from io import BytesIO

import numpy as np 
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, State, callback, dash_table, dcc, html
from dash_iconify import DashIconify
from PIL import Image

from app_utils.left_panel import left_panel
from app_utils.right_panel import generate_plotly_figure, right_panel
from main_solution import generate_predictions
from utils.variables import SRC_PATH

location_path = SRC_PATH/"app_utils"/"assets"/"data"/"location.csv"
plume_df = pd.read_csv(location_path)
result = None

def parse_contents(content, filename):
    content_type, content_string = content.split(',')
    decoded = base64.b64decode(content_string)
    image = Image.open(BytesIO(decoded))

    # Check if the image is TIF, and convert it to RGB if necessary
    if image.format == 'TIFF':
        image = image.convert('RGB')

    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = "data:image/png;base64," + \
        base64.b64encode(buffered.getvalue()).decode()
    return html.Div([
        html.Div(
            [html.H5(filename)],
            style={"justify-content": "center", "display": "flex"}, id="image_container"),

        html.Div([
            html.Img(src=img_str, style={'width': 'auto', 'height': '50vh'}),
        ], style={"justify-content": "center", "display": "flex"}, id="image_container")

    ])


app = Dash(__name__, external_stylesheets=[
    dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP],
    suppress_callback_exceptions=True,  # comment this line if you want
    #    # to see callback exceptions
    update_title=None,

    #    meta_tags=[{"name": "viewport",
    #                "content": "width=device-width, initial-scale=1"}],
    assets_folder="app_utils/assets"

)

app.layout = dbc.Container(
    [dcc.Input(id='dummy', type='hidden', value=None),
        dbc.Row([
            left_panel(),
            right_panel()
        ])
     ], fluid=True,
    id='app-container')

app.title = "METHALLITE"


########## apps callbacks ##########

@callback(
    Output("global_map_tab", "children"),
    Input("dummy", "value")
)
def initialize_graph(dummy):
    if dummy is None:
        return dcc.Graph(figure=generate_plotly_figure(plume_df), style={'width': '100%', 'height': '90vh'}, config={"scrollZoom": False})


@callback(
    Output('image_tab', 'children'),
    Input('upload_image', 'contents'),
    State('upload_image', 'filename')
)
def update_image(content, name):
    if content is not None:
        children = parse_contents(content, name)
        return children
    else:
        return None


@callback(
    Output("run", "disabled"),
    Input("image_tab", "children"),
)
def check_run_condition(children):
    if children is not None:
        return False
    return True


@callback(
    Output("model_result_tab", "children"),
    State("upload_image", "contents"),
    Input("run", "n_clicks"),
)
def run_prediction(content, n_clicks):
    global result
    if n_clicks:
        content_type, content_string = content.split(',')
        result = generate_predictions(content_string)
        # case1 plume is detected
        if result > 0.5:
            return html.Div([
                html.H3(f"Model result: Plume detected (with probability {round(float(result[0][0]), 2)})", id="model_result"), #np.round(result[0], 2)[0]
                dbc.Row([
                    dbc.Col([dmc.TextInput(label="Latitude", id="latitude"),
                             ]),
                    dbc.Col([dmc.TextInput(label="Longitude", id="longitude"),
                             ]),
                ]),
             
                dmc.Button("Add to map", leftIcon=DashIconify(
                    icon="pepicons-pop:pinpoint-circle"), color="secondary", size="sm", id="add_to_map")
            ])

        else:
            # case no plume is detected on the image
            return html.Div([
                html.H3("Model result: No Plume detected"),
            ])


@callback(
    Output("global_map_tab", "children",  allow_duplicate=True),
    Input("add_to_map", "n_clicks"),
    State("latitude", "value"),
    State("longitude", "value"),
    prevent_initial_call=True
)
def update_map(n_clicks, lat, lon):
    if n_clicks:
        new_df = pd.DataFrame(
            {"lat": [lat], "lon": [lon], "probability": [result[0][0]], "detected": [False]})
        location_df = pd.read_csv(location_path)
        location_df = pd.concat([location_df, new_df], axis=0)
        location_df.to_csv(location_path, index=False)
        return dcc.Graph(figure=generate_plotly_figure(location_df), style={'width': '100%', 'height': '90vh'}, config={"scrollZoom": False})


# run the app

if __name__ == '__main__':
    app.run_server(debug=False, port=8888)
