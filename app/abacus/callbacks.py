from app import app
from dash import dcc, html
import dash_bootstrap_components as dbc
import dash_daq as daq
from dash import Dash, Input, Output, State

from config.config import ConfigFactory, footer, header, nav
from dash import dcc, html

conf = ConfigFactory.factory()


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
