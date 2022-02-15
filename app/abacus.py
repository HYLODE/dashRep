"""
Abacus demo
"""
from dash import dcc, html
import dash_bootstrap_components as dbc
import dash_daq as daq
from dash import Dash, Input, Output, State


from config import ConfigFactory
from config import header, nav, footer

from app import app

def slider(id: str, value=0, min=0, max=5):
    marks = {str(i): str(i) for i in range(min, max+1)}
    slider = daq.Slider(
        id=id,
        min=min,
        max=max,
        value=value,
        step=1,
        marks=marks
    )
    res = html.Div([slider],
                   # now pad below by x% of the viewport height
                   style={'margin-bottom': '2vh'})
    return res


@app.callback(
    # output=dict(json_data=Output("arrivals", "children")),  # output data to store
    Output("arrivals_total", "children"),
    inputs=dict(
        ed=Input("arrivals_ed", "value"),
        pacu_el=Input("arrivals_pacu_el", "value"),
        pacu_em=Input("arrivals_pacu_em", "value"),
        perrt=Input("arrivals_perrt", "value"),
        tx_in=Input("arrivals_transfers_in", "value"),
    ),
)
def admissions_total(ed, pacu_el, pacu_em, perrt, tx_in):
    total = ed + pacu_el + pacu_em + perrt + tx_in
    return f'{total} admissions today'


card_ed = dbc.Card(
    [
        dbc.CardHeader("Emergency Department"),
        dbc.CardBody(
            [
                html.P("Predicted admissions", className="card-text"),
                slider("arrivals_ed"),

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
                slider("arrivals_pacu_el"),

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
                slider("arrivals_pacu_em"),

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
                slider("arrivals_perrt"),

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
                slider("arrivals_transfers_in"),

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
                    html.Div(id="arrivals_total"),

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
