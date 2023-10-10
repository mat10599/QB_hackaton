import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import pandas as pd
from dash import Dash, Input, Output, State, callback, dcc, html, dash_table
from dash_iconify import DashIconify
import datetime
import base64
from PIL import Image
from io import BytesIO


def parse_contents(content, filename):
    content_type, content_string = content.split(',')
    decoded = base64.b64decode(content_string)
    image = Image.open(BytesIO(decoded))

    # Check if the image is TIF, and convert it to RGB if necessary
    if image.format == 'TIFF':
        image = image.convert('RGB')
    
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = "data:image/png;base64," + base64.b64encode(buffered.getvalue()).decode()
    return html.Div([
        html.H5(filename),

        # HTML images accept base64 encoded strings in the same format
        # that is supplied by the upload
        # transform tif content into png content
        
        html.Div([
        html.Img(src=img_str, style={'width': '500px', 'height': 'auto'}),
        ], style={"justify-content": "center", "display": "flex"}),

    ])


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
                    "Global Map",
                    icon=DashIconify(icon="mingcute:earth-2-line"),
                    value="global_map",
                ),
            ]),
            dmc.TabsPanel(value="image", id="image_tab"),
            dmc.TabsPanel(value="global_map", id="global_map_tab")
        ],
            value="image",
        )
    ], id="results")


def coordinate_input(text, id):
    return dbc.Row([
        dbc.Col([
            dmc.TextInput(
                label=f"{text}", id=id)
        ])
    ])


def run():
    return dbc.Row([
        dbc.Col([
            dmc.Center(
            dmc.Button("Run", leftIcon=DashIconify(icon="ph:play-fill"), size="xl",
                   color="primary", id="run", disabled=True, loading=False,
                       )
            )
        ])
    ], id="row_run")


def upload():
    return dbc.Row([
        dbc.Col([
            dcc.Upload(
                id="upload_image",
                children=html.Div([
                    'Drag and Drop',
                    html.Br(),
                    "Or ",
                    html.Br(),
                    html.A('Select Image', style={
                           "text-decoration": "underline"})
                ]),
                style={
                    'min-height': '300px',
                    'lineHeight': '45px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px',
                    'display': 'flex',
                    "font-size": "25px"

                },
    
                # Allow multiple files to be uploaded
                multiple=False,
                className="justify-content-center align-items-center vertical-align-center"
                # disabled=False
            )
        ])
    ])


def left_panel():
    return dbc.Col([
        html.H1("Methane Plume Detector Application", id="title"),
        upload(),
        run()
    ],
        width=3,
        id="left_column"
    )


def right_panel():
    return dbc.Col([
        result()
    ], id="right_column")


app = Dash(__name__, external_stylesheets=[
           dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP],
           #    suppress_callback_exceptions=True,  # comment this line if you want
           #    # to see callback exceptions
           update_title=None,
           #    meta_tags=[{"name": "viewport",
           #                "content": "width=device-width, initial-scale=1"}],
           assets_folder="app_utils/assets"

           )

app.layout = dbc.Container(
    [
        dbc.Row([
            left_panel(),
            right_panel()
        ])
    ], fluid=True,
    id='app-container')

app.title = "QR plume detection"


########## apps callbacks ##########

@callback(Output('image_tab', 'children'),
              Input('upload_image', 'contents'),
              State('upload_image', 'filename')
)
def update_output(content, name):
    if content is not None:
        children = parse_contents(content, name)
        return children

@callback(
    Output("run", "disabled"),
    Input("image_tab", "children"),
)
def check_run_condition(children):
    if children is not None:
        return False
    return True

@callback(
    Output("")
)


# run the app

if __name__ == '__main__':
    app.run_server(debug=True, port=8888)
