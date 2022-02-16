"""
Abacus demo
TODO: demonstrate DEMAND by working with open beds so allow the total to exceed the available
"""
from app import app
from dash import dcc, html
import dash_bootstrap_components as dbc

from config.config import ConfigFactory, footer, header, nav

conf = ConfigFactory.factory()

from . import callbacks



# ============
# Patients IN
# ============


card_ed = dbc.Card(
    [
        dbc.CardHeader("Emergency Department"),
        dbc.CardBody(
            [
                html.P("Predicted admissions", className="card-text"),
                callbacks.slider("plus_ed"),

            ]
        ),
    ],
)

card_pacu_el = dbc.Card(
    [
        dbc.CardHeader("Surgery - Elective"),
        dbc.CardBody(
            [
                html.P("Predicted admissions", className="card-text"),
                callbacks.slider("plus_pacu_el"),

            ]
        ),
    ],
)

card_pacu_em = dbc.Card(
    [
        dbc.CardHeader("Surgery - Emergency"),
        dbc.CardBody(
            [
                html.P("Predicted admissions", className="card-text"),
                callbacks.slider("plus_pacu_em"),

            ]
        ),
    ],
)

card_perrt = dbc.Card(
    [
        dbc.CardHeader("PERRT"),
        dbc.CardBody(
            [
                html.P("Predicted admissions", className="card-text"),
                callbacks.slider("plus_perrt"),

            ]
        ),
    ],
)


card_transfer_in = dbc.Card(
    [
        dbc.CardHeader("External Transfers"),
        dbc.CardBody(
            [
                html.P("Predicted admissions", className="card-text"),
                callbacks.slider("plus_transfers"),

            ]
        ),
    ],
)

# ================
# Current patients
# ================

card_patients = dbc.Card(
    [
        dbc.CardHeader("Patient list"),
        dbc.CardBody(
            [
                html.P("Current census", className="card-text"),
                callbacks.slider_census(),
                # html.Div(id="abacus-census-slider-div"),
                # callbacks.slider("census_now", value=callbacks.count_patients_in_datatable(), max=35),
                html.Div(id="abacus-datatable-main"),

            ]
        ),
    ],
)

# ============
# Patients out
# ============

card_stepdowns = dbc.Card(
    [
        dbc.CardHeader("Ward step downs"),
        dbc.CardBody(
            [
                html.P("Predicted discharges", className="card-text"),
                callbacks.slider("minus_step_down"),

            ]
        ),
    ],
)

card_discharges = dbc.Card(
    [
        dbc.CardHeader("Discharge Home"),
        dbc.CardBody(
            [
                html.P("Predicted discharges", className="card-text"),
                callbacks.slider("minus_discharges"),

            ]
        ),
    ],
)

card_transfer_out = dbc.Card(
    [
        dbc.CardHeader("Transfer out"),
        dbc.CardBody(
            [
                html.P("Predicted discharges", className="card-text"),
                callbacks.slider("minus_transfers"),

            ]
        ),
    ],
)

card_eol = dbc.Card(
    [
        dbc.CardHeader("End of life"),
        dbc.CardBody(
            [
                html.P("Predicted discharges", className="card-text"),
                callbacks.slider("minus_eol"),

            ]
        ),
    ],
)


main = html.Div([
    dbc.Row(dbc.Col([
        html.Div("Full width row"),
        html.Div(id="census_next_display"),
    ])),

    dbc.Row([
            dbc.Col(
                [
                    html.H3("Admissions"),
                    html.Div(id="plus_total_display"),

                ]),

            dbc.Col(
                [
                    html.H3("Current patients"),
                    html.Div(id="census_now_display"),
                ]),

            dbc.Col(
                [
                    html.H3("Discharges"),
                    html.Div(id="minus_total_display"),
                ]),
            ],
            ),

    dbc.Row([
            dbc.Col(
                [
                    # Admissions
                    card_pacu_el,
                    card_pacu_em,
                    card_ed,
                    card_perrt,
                    card_transfer_in,
                ]),

            dbc.Col(
                [
                    # Current patients
                    card_patients,
                ]),

            dbc.Col(
                [
                    # Discharges & stepdowns etc
                    card_stepdowns,
                    card_discharges,
                    card_transfer_out,
                    card_eol,
                ]),
            ],
            ),
])

# use this to store dash components that you don't need to 'see'
dash_only = html.Div(
    [

        dcc.Store(id="plus_total"),
        dcc.Store(id="minus_total"),

        dcc.Interval(id="abacus-interval-data", interval=conf.REFRESH_INTERVAL, n_intervals=0),
        dcc.Store(id="abacus-source-data"),
    ]
)

abacus = dbc.Container(
    fluid=True,
    children=[
        header,
        nav,
        main,
        footer,
        dash_only,
    ],
)
