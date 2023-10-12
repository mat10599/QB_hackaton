import base64

from io import BytesIO


import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import pandas as pd

from dash import Dash, Input, Output, State, callback, dcc, html
from dash_iconify import DashIconify
from PIL import Image

from app_utils.left_panel import left_panel
from app_utils.right_panel import generate_plotly_figure, right_panel
from main_solution import generate_predictions
from utils.variables import SRC_PATH

# define useful variables and paths
location_path = SRC_PATH/"app_utils"/"assets"/"data"/"location.csv"
plume_df = pd.read_csv(location_path)
result = None

# helper function


def parse_contents(content, filename):
    """parse the content of the dash uploader and transform the greyscale
    image to RGB

    Args:
        content (_type_): content of the dcc uploder
        filename (_type_): name of the file being uploaded

    Returns:
        html.Div: html div containing the image and its title
    """
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
            style={"justify-content": "center", "display": "flex"},
            id="image_container"),

        html.Div([
            html.Img(src=img_str, style={'width': 'auto', 'height': '50vh'}),
        ], style={"justify-content": "center", "display": "flex"},
            id="image_container")

    ])


# define the app
app = Dash(__name__, external_stylesheets=[
    dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP],
    suppress_callback_exceptions=True,
    update_title=None,
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

app.title = "Methallite"


# apps callbacks #

@callback(
    Output("global_map_tab", "children"),
    Input("dummy", "value")
)
def initialize_graph(dummy):
    """takes the content of dummy object and return the inital
    graph. This graph contains the historical data with the plume data
    previously added by the user using the app

    Args:
        dummy (str): None if initialization step else "dummy"

    Returns:
        _type_: the inital graph
    """
    if dummy is None:
        return dcc.Graph(figure=generate_plotly_figure(plume_df),
                         style={'width': '100%', 'height': '90vh'},
                         config={"scrollZoom": False})


@callback(
    Output('image_tab', 'children'),
    Input('upload_image', 'contents'),
    State('upload_image', 'filename')
)
def update_image(content, name):
    """prints the image in the result image tab

    Args:
        content (_type_): image description
        name (str): name of the file

    Returns:
        html.Div: the image and the file name
    """
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
    """checks that the image has been uploaded before enabling the run button
    """
    if children is not None:
        return False
    return True


@callback(
    Output("model_result_tab", "children"),
    State("upload_image", "contents"),
    Input("run", "n_clicks"),
)
def run_prediction(content, n_clicks):
    """runs model prediction when the user clicks on run button

    Args:
        content (_type_): image object
        n_clicks (int): number of clicks on the run button

    Returns:
        html.Div: Model result
    """
    global result
    if n_clicks:
        content_type, content_string = content.split(',')
        result = generate_predictions(content_string)
        # case1 plume is detected
        if result > 0.5:
            return html.Div([
                # np.round(result[0], 2)[0]
                html.H3(
                    f"""Model result: Plume detected (with probability {
                        round(float(result[0][0]), 2)})""", id="model_result"),
                dbc.Row([
                    dbc.Col([dmc.TextInput(label="Latitude", id="latitude"),
                             ]),
                    dbc.Col([dmc.TextInput(label="Longitude", id="longitude"),
                             ]),
                ]),

                dmc.Button("Add to map", leftIcon=DashIconify(
                    icon="pepicons-pop:pinpoint-circle"), color="secondary",
                    size="sm", id="add_to_map")
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
def update_map(n_clicks, lat, lon) -> dcc.Graph:
    """updates the graph by adding the new plume location

    Args:
        n_clicks int): num of clicks on the add to map button
        lat (float): latitude of the plume
        lon (float): longitude of the plume

    Returns:
        dcc.Graph: Graph object
    """
    if n_clicks:
        new_df = pd.DataFrame(
            {"lat": [lat], "lon": [lon], "probability": [result[0][0]],
             "detected": [False]})
        location_df = pd.read_csv(location_path)
        location_df = pd.concat([location_df, new_df], axis=0)
        location_df.to_csv(location_path, index=False)
        return dcc.Graph(figure=generate_plotly_figure(location_df),
                         style={'width': '100%', 'height': '90vh'},
                         config={"scrollZoom": False})


# run the app

if __name__ == '__main__':
    app.run_server(debug=False, port=8888)
