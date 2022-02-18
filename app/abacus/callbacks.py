import pandas as pd

from dash import dcc, html
from dash import Input, Output
from dash import dash_table as dt

import dash_bootstrap_components as dbc

from app import app
from config.config import ConfigFactory

# use the function from sitrep to pull and clean data
from sitrep.callbacks import request_data
from utils import utils

conf = ConfigFactory.factory()


@app.callback(
    output=dict(json_data=Output("abacus-source-data", "data")),
    inputs=dict(intervals=Input("abacus-interval-data", "n_intervals"), ),
    # prevent_initial_call=True,  # suppress_callback_exceptions does not work
)
def data_io(intervals):
    """
    stores the data in a dcc.Store
    runs on load and will be triggered each time the table is updated or the REFRESH_INTERVAL elapses
    """
    ward = 'T03'  # placeholder hardcoded; need to move to selection
    ward = ward.lower()
    df = request_data(ward)
    print(df.head())
    return dict(json_data=df.to_dict("records"))


@app.callback(
    Output("abacus-datatable-main", "children"),
    Input("abacus-source-data", "data"),
)
def gen_datatable_main(json_data):

    # datatable defined by columns and by input data
    # abstract this to function so that you can guarantee the same data each time

    COL_DICT = [
        {"name": v, "id": k} for k, v in conf.COLS.items() if k in conf.COLS_FULL
    ]

    # prepare properties of columns
    # updates b/c list are mutable
    utils.deep_update(
        utils.get_dict_from_list(COL_DICT, "id", "wim_1"), dict(editable=True)
    )
    utils.deep_update(
        utils.get_dict_from_list(COL_DICT, "id", "discharge_ready_1_4h"),
        dict(editable=True),
    )
    utils.deep_update(
        utils.get_dict_from_list(COL_DICT, "id", "discharge_ready_1_4h"),
        dict(presentation="dropdown"),
    )

    DISCHARGE_OPTIONS = ["Ready", "No", "Review"]

    dto = (
        dt.DataTable(
            id="tbl-main",
            columns=COL_DICT,
            data=json_data,
            editable=False,
            dropdown={
                "discharge_ready_1_4h": {
                    "options": [{"label": i, "value": i} for i in DISCHARGE_OPTIONS],
                    "clearable": False,
                },
            },
            # style_as_list_view=True,  # remove col lines
            style_cell={
                "fontSize": 12,
                # 'font-family':'sans-serif',
                "padding": "3px",
            },
            style_cell_conditional=[
                {"if": {"column_id": "bay"}, "textAlign": "right"},
                {"if": {"column_id": "bed"}, "textAlign": "left"},
                {"if": {"column_id": "name"}, "textAlign": "left"},
                {"if": {"column_id": "name"}, "fontWeight": "bolder"},
                {"if": {"column_id": "discharge_ready_1_4h"}, "textAlign": "left"},
            ],
            style_data={"color": "black", "backgroundColor": "white"},
            # striped rows
            style_data_conditional=[
                {
                    "if": {"row_index": "odd"},
                    "backgroundColor": "rgb(220, 220, 220)",
                }
            ],
            sort_action="native",
            cell_selectable=True,  # possible to click and navigate cells
            # row_selectable="single",
        ),
    )

    # wrap in container
    dto = [
        dbc.Container(
            dto,
            className="dbc",
        )
    ]
    return dto


def slider_census():
    ward = 'T03'.lower()
    df = request_data(ward)
    value =  df['mrn'].nunique()
    _min, _max, _step = 0, 36, 5
    marks = {str(i): str(i) for i in range(_min, _max+1, _step)}
    slider = dcc.Slider(
        id="abacus-census-slider",
        min=_min,
        max=_max,
        value=value,
        marks=marks,
        step=1, # i.e. patients are integers
        updatemode="drag",
        tooltip={"placement": "top", "always_visible": True},
    )
    return slider



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
        Input("abacus-census-slider", "value"),
    ]
)
def display_census_now(census_now):
    total = str(census_now)
    return [html.Div(f"{total} census now")]


@app.callback(
    [Output("census_next_display", "children")],
    [
        Input("abacus-census-slider", "value"),
        Input("plus_total", "data"),
        Input("minus_total", "data"),
    ]
)
def display_census_next(census_now, plus_total, minus_total):
    census_now = int(census_now)
    total = str(census_now + plus_total - minus_total)
    # TODO: colour the alert wrt to the maximum available beds
    return [dbc.Alert(f"{total} calculated census tomorrow", color="danger")]
