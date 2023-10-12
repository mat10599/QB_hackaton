import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import Dash, Input, Output, State, callback, dcc, html, dash_table
from dash_iconify import DashIconify


def coordinate_input(text, id):
    return dbc.Row([
        dbc.Col([
            dmc.TextInput(
                label=f"{text}", id=id)
        ])
    ])

# def image_info():
#     return dbc.Row([
#         dbc.Col([
#         ], id="file_name")
#     ])

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
                    'lineHeight': '45px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px',
                    'display': 'flex',
                    "font-size": "25px",
                    "min-width": "300px",
                    "height": "40vh"

                },
    
                # Allow multiple files to be uploaded
                multiple=False,
                className="justify-content-center align-items-center vertical-align-center"
                # disabled=False
            )
        ])
    ])


def title():
    return dbc.Row([
        dbc.Col([
            html.Img(src="assets/images/logo.svg", height="100px")
        ],
        width=1),
    
        dbc.Col([
            html.H2("Methane Plume Detector Application", id="title")
        ])
    ])


def left_panel():
    return dbc.Col([
        title(),
        upload(),
        # image_info(),
        run()
    ],
        width=3,
        id="left_column"
    )



