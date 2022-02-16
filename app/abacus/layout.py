"""
Abacus demo
TODO: demonstrate DEMAND by working with open beds so allow the total to exceed the available
"""
from dash import dcc, html
import dash_bootstrap_components as dbc
import dash_daq as daq
from dash import Dash, Input, Output, State

from config.config import ConfigFactory, footer, header, nav
from dash import dcc, html

conf = ConfigFactory.factory()


from app import app


def slider(id: str, value=0, min=0, max=5):
    marks = {str(i): str(i) for i in range(min, max+1)}
    slider = dcc.Slider(
        id=id,
        min=min,
        max=max,
        value=value,
        step=1,
        marks=marks,
        updatemode="drag",
        tooltip={"placement": "top", "always_visible": True},
    )
    res = html.Div([slider],
                   # now pad below by x% of the viewport height
                   style={'margin-bottom': '2vh'})
    return res


@app.callback(
    [Output("plus_total", "data")],
    [
        Input("plus_ed", "value"),
        Input("plus_pacu_el", "value"),
        Input("plus_pacu_em", "value"),
        Input("plus_perrt", "value"),
        Input("plus_transfers", "value"),
    ],
)
def store_plus_total(ed, pacu_el, pacu_em, perrt, tx_in, ):
    total = (ed + pacu_el + pacu_em + perrt + tx_in)
    return (total, )


@app.callback(
    [Output("plus_total_display", "children")],
    [Input("plus_total", "data")]
)
def display_plus_total(plus_total):
    total = str(plus_total)
    return [html.Div(f"{total} admissions today")]


@app.callback(
    [Output("minus_total", "data")],
    [
        Input("minus_step_down", "value"),
        Input("minus_discharges", "value"),
        Input("minus_transfers", "value"),
        Input("minus_eol", "value"),
    ]
)
def store_minus_total(step_down, discharges, tx_out, eol, ):
    total = step_down + discharges + tx_out + eol
    return (total, )


@app.callback(
    [Output("minus_total_display", "children")],
    [Input("minus_total", "data")]
)
def display_minus_total(minus_total):
    total = str(minus_total)
    return [html.Div(f"{total} discharges today")]


@app.callback(
    [Output("census_now_display", "children")],
    [
        Input("census_now", "value"),
    ]
)
def display_census_now(census_now):
    total = str(census_now)
    return [html.Div(f"{total} census now")]


@app.callback(
    [Output("census_next_display", "children")],
    [
        Input("census_now", "value"),
        Input("plus_total", "data"),
        Input("minus_total", "data"),
    ]
)
def display_census_next(census_now, plus_total, minus_total):
    total = str(census_now + plus_total - minus_total)
    return [html.Div(f"{total} census tomorrow")]

# ============
# Patients IN
# ============


card_ed = dbc.Card(
    [
        dbc.CardHeader("Emergency Department"),
        dbc.CardBody(
            [
                html.P("Predicted admissions", className="card-text"),
                slider("plus_ed"),

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
                slider("plus_pacu_el"),

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
                slider("plus_pacu_em"),

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
                slider("plus_perrt"),

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
                slider("plus_transfers"),

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
                slider("census_now", value=30, max=35),

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
                slider("minus_step_down"),

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
                slider("minus_discharges"),

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
                slider("minus_transfers"),

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
                slider("minus_eol"),

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
