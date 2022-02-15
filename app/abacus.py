"""
Abacus demo
"""
from dash import dcc, html
import dash_bootstrap_components as dbc

from config import ConfigFactory
from config import header, nav, footer

card_ed = dbc.Card(
    [
        dbc.CardHeader("Emergency Department"),
        dbc.CardBody(
            [
                html.H4("Card title",
                        className="card-title"),
                html.P("This is some card text",
                       className="card-text"),
            ]
        ),
    ],
)

card_pacu_el = dbc.Card(
    [
        dbc.CardHeader("Surgery - Elective"),
        dbc.CardBody(
            [
                html.H4("Card title",
                        className="card-title"),
                html.P("This is some card text",
                       className="card-text"),
            ]
        ),
    ],
)

card_pacu_em = dbc.Card(
    [
        dbc.CardHeader("Surgery - Emergency"),
        dbc.CardBody(
            [
                html.H4("Card title",
                        className="card-title"),
                html.P("This is some card text",
                       className="card-text"),
            ]
        ),
    ],
)

card_perrt = dbc.Card(
    [
        dbc.CardHeader("PERRT"),
        dbc.CardBody(
            [
                html.H4("Card title",
                        className="card-title"),
                html.P("This is some card text",
                       className="card-text"),
            ]
        ),
    ],
)


card_transfer_in = dbc.Card(
    [
        dbc.CardHeader("External Transfers"),
        dbc.CardBody(
            [
                html.H4("Card title",
                        className="card-title"),
                html.P("This is some card text",
                       className="card-text"),
            ]
        ),
    ],
)

card_patients = dbc.Card(
    [
        dbc.CardHeader("Patient list"),
        dbc.CardBody(
            [
                html.H4("Card title",
                        className="card-title"),
                html.P("This is some card text",
                       className="card-text"),
            ]
        ),
    ],
)

card_stepdowns = dbc.Card(
    [
        dbc.CardHeader("Ward step downs"),
        dbc.CardBody(
            [
                html.H4("Card title",
                        className="card-title"),
                html.P("This is some card text",
                       className="card-text"),
            ]
        ),
    ],
)

card_discharges = dbc.Card(
    [
        dbc.CardHeader("Discharge Home"),
        dbc.CardBody(
            [
                html.H4("Card title",
                        className="card-title"),
                html.P("This is some card text",
                       className="card-text"),
            ]
        ),
    ],
)

card_transfer_out = dbc.Card(
    [
        dbc.CardHeader("Transfer out"),
        dbc.CardBody(
            [
                html.H4("Card title",
                        className="card-title"),
                html.P("This is some card text",
                       className="card-text"),
            ]
        ),
    ],
)

card_eol = dbc.Card(
    [
        dbc.CardHeader("End of life"),
        dbc.CardBody(
            [
                html.H4("Card title",
                        className="card-title"),
                html.P("This is some card text",
                       className="card-text"),
            ]
        ),
    ],
)

main = html.Div([
    dbc.Row(dbc.Col(html.Div("Full width row"))),

    dbc.Row([
            dbc.Col(
                [
                    html.H3("Admissions"),
                ]),

            dbc.Col(
                [
                    html.H3("Current patients"),
                ]),

            dbc.Col(
                [
                    html.H3("Discharges"),
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


abacus = dbc.Container(
    fluid=True,
    children=[
        header,
        nav,
        main,
        footer,
        # dash_only,
    ],
)
