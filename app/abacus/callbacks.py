import dash_bootstrap_components as dbc
import pandas as pd
from config.config import ConfigFactory
from dash import Input, Output
from dash import dash_table as dt
from dash import dcc, html
# from ed.ed import get_dataframe, filter_same, prepare_ridge_densities
from ed import ed
import plotly.graph_objects as go
# from ridgeplot import ridgeplot
# use the function from sitrep to pull and clean data
from sitrep.callbacks import request_data

from app import app
from utils import utils

conf = ConfigFactory.factory()


# ****************************************************************************
# *                        emergency department demand                       *
# ****************************************************************************


@app.callback(
    Output("abacus-ed-demand", "children"),
    Input("abacus-interval-data", "n_intervals"),
    Input("plus_ed", "value"),
)
def ed_demand_plot(json_data, ed_slider):
    df = ed.get_dataframe(
        sql_script=ed.AGG_SQL_FILE,
        csv_file=ed.AGG_CSV_FILE,
        dev=conf.DEV,
        parse_dates=ed.AGG_PARSE_DATES,
    )
    df = ed.wrangle_ed_agg(df)
    df = ed.filter_same(df)

    fig = go.Figure()
    for i in df['days'].unique():
        dfi = df[df['days'] == i]

        colour = 'rgba(255,38,0,1)' if i == 0 else 'rgba(0,0,0,0.2)'
        fig.add_trace(go.Scatter(
            x=dfi['num_adm_pred'] / 10,
            y=dfi['probs'],
            mode="lines",
            marker_color=colour,
        ))

    fig.add_shape(type='line',
                  x0=ed_slider, y0=0,
                  x1=ed_slider, y1=df['probs'].max(),
                  line=dict(color="blue")
                  )
    fig.update_xaxes(range=[0, 4])
    fig.update_layout(showlegend=False)
    fig.update_layout(xaxis_title="Predicted ICU bed demand", yaxis_title="")
    fig.update_layout(template="plotly_white")
    fig.update_layout(height=300)
    config = {
        "displayModeBar": False,
        "staticPlot": True,
        "autosizable": True,
    }
    return dcc.Graph(figure=fig, config=config)


# ****************************************************************************
# *                                 stepdowns                                *
# ****************************************************************************


@app.callback(
    Output("abacus-data-stepdowns", "data"),
    Input("abacus-tbl-census", "data"),
)
def read_discharges(census_json) -> dict:
    """
    Reads from the main census table those patients with a discharge flag
    Returns just that filtered list


    :param      census_json:  The census json
    :type       census_json:  str

    :returns:   { description_of_the_return_value }
    :rtype:     str
    """
    # Look for discharges
    DISCHARGE_OPTIONS = ["Ready", "No", "Review"]

    df = pd.DataFrame.from_records(census_json)
    df = df[df["discharge_ready_1_4h"] == "Ready"]
    return df.to_dict("records")


@app.callback(
    Output("abacus-stepdowns-datatable", "children"),
    Input("abacus-data-stepdowns", "data"),
)
def gen_datatable_stepdowns(stepdowns_json):
    # df = pd.DataFrame.from_records(stepdowns_json)
    _cols = ["bed", "name"]
    COL_DICT = [{"name": v, "id": k}
                for k, v in conf.COLS.items() if k in _cols]

    dto = (
        dt.DataTable(
            id="abacus-tbl-stepdowns",
            columns=COL_DICT,
            data=stepdowns_json,
            editable=False,
            style_as_list_view=True,  # remove col lines
            style_cell={
                "fontSize": 12,
                # 'font-family':'sans-serif',
                "padding": "3px",
            },
            style_cell_conditional=[
                # {"if": {"column_id": "bay"}, "textAlign": "right"},
                # {"if": {"column_id": "bed"}, "textAlign": "left"},
                {"if": {"column_id": "name"}, "textAlign": "left"},
                {"if": {"column_id": "name"}, "fontWeight": "bolder"},
                # {"if": {"column_id": "discharge_ready_1_4h"}, "textAlign": "left"},
            ],
            style_data={"color": "black", "backgroundColor": "white"},
            # striped rows
            style_data_conditional=[
                {
                    "if": {"row_index": "odd"},
                    "backgroundColor": "rgb(220, 220, 220)",
                }
            ],
            # sort_action="native",
            # cell_selectable=True,  # possible to click and navigate cells
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


# ****************************************************************************
# *                          load main census table                          *
# ****************************************************************************


@app.callback(
    output=dict(json_data=Output("abacus-source-data", "data")),
    inputs=dict(
        intervals=Input("abacus-interval-data", "n_intervals"),
    ),
    # prevent_initial_call=True,  # suppress_callback_exceptions does not work
)
def data_io(intervals):
    """
    stores the data in a dcc.Store
    runs on load and will be triggered each time the table is updated or the REFRESH_INTERVAL elapses
    """
    ward = "T03"  # placeholder hardcoded; need to move to selection
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
            id="abacus-tbl-census",
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


# ****************************************************************************
# *                                  sliders                                 *
# ****************************************************************************


def slider_census():
    ward = "T03".lower()
    df = request_data(ward)
    value = df["mrn"].nunique()
    _min, _max, _step = 0, 36, 5
    marks = {str(i): str(i) for i in range(_min, _max + 1, _step)}
    slider = dcc.Slider(
        id="abacus-census-slider",
        min=_min,
        max=_max,
        value=value,
        marks=marks,
        step=1,  # i.e. patients are integers
        updatemode="drag",
        tooltip={"placement": "top", "always_visible": True},
    )
    return slider


def slider(id: str, value=0, min=0, max=5):
    marks = {str(i): str(i) for i in range(min, max + 1)}
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
    res = html.Div(
        [slider],
        # now pad below by x% of the viewport height
        style={"margin-bottom": "2vh"},
    )
    return res


# ****************************************************************************
# *                                  Pluses                                  *
# ****************************************************************************


@app.callback(
    [Output("plus_total", "data")],
    [
        Input("plus_ed", "value"),
        Input("plus_pacu_el", "value"),
        Input("plus_pacu_em", "value"),
        Input("plus_perrt", "value"),
        Input("plus_transfers", "value"),
    ],
    prevent_initial_call=True,  # suppress_callback_exceptions does not work
)
def store_plus_total(
    ed,
    pacu_el,
    pacu_em,
    perrt,
    tx_in,
):
    total = ed + pacu_el + pacu_em + perrt + tx_in
    return (total,)


@app.callback(
    [Output("plus_total_display", "children")],
    # suppress_callback_exceptions does not work
    [Input("plus_total", "data")],     prevent_initial_call=True,
)
def display_plus_total(plus_total):
    total = str(plus_total)
    msg = f"{total} Admissions budgeted today"
    card = dbc.Card(
        [
            dbc.CardHeader(msg, className="card-title")
        ],
        color="dark",
        inverse=True,
        style={"margin-top": "1vh"},
    )
    return (card, )


# ****************************************************************************
# *                                 # Minuses                                *
# ****************************************************************************


@app.callback(
    [Output("minus_total", "data")],
    [
        # Input("minus_step_down", "value"),
        Input("abacus-data-stepdowns", "data"),
        Input("minus_discharges", "value"),
        Input("minus_transfers", "value"),
        Input("minus_eol", "value"),
    ],
)
def store_minus_total(
    step_downs_json,
    discharges,
    tx_out,
    eol,
):
    # import pdb; pdb.set_trace()
    # df_stepdowns = pd.DataFrame.from_records(step_downs_json)
    if step_downs_json is None:
        step_downs_n = 0
    else:
        step_downs_n = len(step_downs_json)
    total = step_downs_n + discharges + tx_out + eol
    return (total,)


@app.callback(
    [Output("minus_total_display", "children")], [Input("minus_total", "data")]
)
def display_minus_total(minus_total):
    total = str(minus_total)
    msg = f"{total} Discharges budgeted today"
    card = dbc.Card(
        [
            dbc.CardHeader(msg, className="card-title")
        ],
        color="dark",
        inverse=True,
        style={"margin-top": "1vh"},
    )
    return (card, )


# ****************************************************************************
# *                              running totals                              *
# ****************************************************************************


@app.callback(
    [Output("census_now_display", "children")],
    [
        Input("abacus-census-slider", "value"),
    ],
)
def display_census_now(census_now):
    total = str(census_now)
    msg = f"{total} current patients"
    card = dbc.Card(
        [
            dbc.CardHeader(msg, className="card-title")
        ],
        color="dark",
        inverse=True,
        style={"margin-top": "1vh"},
    )
    return (card, )


@app.callback(
    [Output("census_next_display", "children")],
    [
        Input("abacus-census-slider", "value"),
        Input("plus_total", "data"),
        Input("minus_total", "data"),
    ],
    prevent_initial_call=True,  # suppress_callback_exceptions does not work
)
def display_census_next(census_now, plus_total, minus_total):
    census_now = int(census_now)
    # var or 0 handles events that returns None
    total = str(
        ((census_now or 0)
            + (plus_total or 0)
            - (minus_total or 0)))

    msg = f"{total} calcualted census in 24h"

    card = dbc.Card(
        [
            dbc.CardHeader(msg, className="card-title")
        ],
        color="danger",
        inverse=True,
        style={"margin-top": "1vh"},
    )
    return (card, )
