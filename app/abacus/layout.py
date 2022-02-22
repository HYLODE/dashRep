"""
Abacus demo
TODO: demonstrate DEMAND by working with open beds so allow the total to exceed the available
"""
from abacus.main_census import main_census_card
from abacus.transfers_in import transfers_in_card

import dash_bootstrap_components as dbc

from . import callbacks
from app import app
from dash import dcc
from dash import html

from config.config import ConfigFactory
from config.config import footer
from config.config import header
from config.config import nav

conf = ConfigFactory.factory()


# ****************************************************************************
# *                             Bed demand INPUTS                            *
# ****************************************************************************


card_ed = dbc.Card(
    [
        dbc.Button("Emergency Department", className="d-grid",
                   href="/ed", color="info"),
        dbc.CardBody(
            [
                # html.P("Predicted admissions", className="card-text"),
                callbacks.slider("plus_ed"),
                html.Div(id="abacus-ed-demand"),

            ]
        ),
    ],
    color="info",  # use colors to dynamically warn of pressure/demand
    outline=True,
)

card_pacu_el = dbc.Card(
    [
        dbc.Button("Surgery - Elective", className="d-grid",
                   href="/pacu-el", disabled=True, color="warning"),
        dbc.CardBody(
            [
                html.P("Predicted admissions", className="card-text"),
                callbacks.slider("plus_pacu_el"),

            ]
        ),
    ],
    color="warning",  # use colors to dynamically warn of pressure/demand
    outline=True,
)

card_pacu_em = dbc.Card(
    [
        # dbc.CardHeader("Surgery - Emergency"),
        dbc.Button("Surgery - Emergency", className="d-grid",
                   href="/pacu-el", disabled=True),
        dbc.CardBody(
            [
                html.P("Predicted admissions", className="card-text"),
                callbacks.slider("plus_pacu_em"),

            ]
        ),
    ],
    color="light",  # use colors to dynamically warn of pressure/demand
    outline=True,
)

card_perrt = dbc.Card(
    [
        dbc.Button("PERRT", className="d-grid", href="/perrt", disabled=True),
        dbc.CardBody(
            [
                html.P("Predicted admissions", className="card-text"),
                callbacks.slider("plus_perrt"),

            ]
        ),
    ],
    # color="light", # use colors to dynamically warn of pressure/demand
    outline=True,
)


card_transfer_in = dbc.Card(
    [
        # dbc.CardHeader(dbc.CardLink("External Transfers", href="/covid")),
        dbc.Button("External Transfers", className="d-grid",
                   href="/covid", disabled=False),
        transfers_in_card,
        # dbc.CardBody(
        #     [
        #         # html.P("Predicted admissions", className="card-text"),
        #         # callbacks.slider("plus_transfers"),

        #     ]
        # ),
    ],
    # color="light", # use colors to dynamically warn of pressure/demand
    outline=True,
)

# ================
# Current patients
# ================

card_patients = dbc.Card(
    [
        dbc.CardHeader("Patient list"),
        dbc.CardBody( [ main_census_card, ] ),
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
                # TODO: add a nice numeric indicator
                html.P("Ready for ward stepdown", className="card-text"),
                # callbacks.slider("minus_step_down"),
                html.Div(id="abacus-stepdowns-datatable"),

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

# ****************************************************************************
# * BEGIN:                         Main layout                               *
# ****************************************************************************


main = html.Div([


    # ****************************************************************************
    # *                      Row 1: Current census                               *
    # ****************************************************************************
    dbc.Row([
            dbc.Col(
                [
                    # html.H3("Admissions"),
                    html.Div(id="plus_total_display"),

                ], md=3),

            dbc.Col(
                [
                    # html.H3("Current patients"),
                    html.Div(id="census_now_display"),
                ], md=6),

            dbc.Col(
                [
                    # html.H3("Discharges"),
                    html.Div(id="minus_total_display"),
                ], md=3),
            ],
            ),

    # ****************************************************************************
    # *                      Row 2: Predicted census in 24hr                     *
    # ****************************************************************************

    dbc.Row(dbc.Col([
        # html.Div("Ward bed management"),
        html.Div(id="census_next_display"),
    ], md={'offset': 3, 'size': 6})),

    # ****************************************************************************
    # *                      Row 3: Detail cards                                 *
    # ****************************************************************************

    dbc.Row([
            dbc.Col(
                [
                    # Admissions
                    card_pacu_el,
                    card_pacu_em,
                    card_ed,
                    card_perrt,
                    card_transfer_in,
                ], md=3),

            dbc.Col(
                [
                    # Current patients
                    card_patients,
                ], md=6),

            dbc.Col(
                [
                    # Discharges & stepdowns etc
                    card_stepdowns,
                    card_discharges,
                    card_transfer_out,
                    card_eol,
                ], md=3),
            ],
            ),
])

# ****************************************************************************
# * END  :                         Main layout                               *
# ****************************************************************************


# use this to store dash components that you don't need to 'see'
dash_only = html.Div(
    [

        dcc.Store(id="plus_total"),
        dcc.Store(id="minus_total"),
        dcc.Store(id="abacus-data-stepdowns"),
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
