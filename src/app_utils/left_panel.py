import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import dcc, html
from dash_iconify import DashIconify


def title():
    return dbc.Row([
        dbc.Col([
            html.Img(src="assets/images/logo.svg", height="100px", id="logo"),
        ],
            width=2),

        dbc.Col([
            html.H3("Methane Plume Detector Application", id="title")
        ])
    ])


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
                className="""justify-content-center align-items-center
                vertical-align-center"""
                # disabled=False
            )
        ])
    ])


def run():
    return dbc.Row([
        dbc.Col([
            dmc.Center(
                dmc.Button("Run", leftIcon=DashIconify(icon="ph:play-fill"),
                           size="xl",
                   color="primary", id="run", disabled=True, loading=False,
                           )
            )
        ])
    ], id="row_run")


def left_panel():
    return dbc.Col([
        title(),
        upload(),
        run()
    ],
        width=3,
        id="left_column"
    )
