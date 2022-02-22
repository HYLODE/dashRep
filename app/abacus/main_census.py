# Simple single card version of the main census module
# Write as standalone here
#
# Requirements
# TODO: simple datatable of the basic census info
# TODO: loop through table and construct string for markdown

import dash
import dash_bootstrap_components as dbc
import pandas as pd

from app import app

from config.config import ConfigFactory
from dash import Dash
from dash import Input
from dash import Output
from dash import State
from dash import dash_table as dt
from dash import dcc
from dash import html

from sitrep.callbacks import request_data
from utils import utils

conf = ConfigFactory.factory()

COLOUR_GREY = "#c0c0c077"
COLOUR_GREEN = "#008000ff"
COLOUR_AMBER = "#ffa500ff"
COLOUR_RED = "#ff0000ff"


def gen_aki_icon(level: str) -> str:
    icon = 'fa fa-flask'
    try:
        level = level.lower()
    except AttributeError:
        level = 'unknown'

    if level == 'false':
        colour = COLOUR_GREY
    elif level == 'true':
        colour = COLOUR_RED
    else:
        colour = COLOUR_GREY
    icon_string = f'<i class="{icon}" style="color: {colour};"></i>'
    return icon_string


def gen_rs_icon(level: str) -> str:
    icon = 'fa fa-lungs'

    try:
        level = level.lower()
    except AttributeError:
        level = 'unknown'

    if level in ['unknown', 'room air']:
        colour = COLOUR_GREY
    elif level in ['oxygen']:
        colour = COLOUR_GREEN
    elif level in ['hfno', 'niv', 'cpap']:
        colour = COLOUR_AMBER
    else:
        colour = COLOUR_RED
    icon_string = f'<i class="{icon}" style="color: {colour};"></i>'
    return icon_string


def gen_cvs_icon(level: str) -> str:
    icon = 'fa fa-heart'
    try:
        n = int(level)
    except ValueError:
        n = 0
    if n == 0:
        colour = COLOUR_GREY
    elif n == 1:
        colour = COLOUR_AMBER
    else:
        colour = COLOUR_RED
    icon_string = f'<i class="{icon}" style="color: {colour};"></i>'
    return icon_string


def make_fake_df(n_rows):
    # run the imports here since this function won't be needed in production
    from faker import Faker
    from faker.providers import DynamicProvider

    infection_status_provider = DynamicProvider(
        provider_name="infection_status",
        elements=['clean', 'COVID', 'ESBL', '']
    )

    fake = Faker('en_GB')
    fake.add_provider(infection_status_provider)
    referrals = []
    for _ in range(n_rows):
        referrals.append(dict(
            name=fake.name(),
            admission_age_years=fake.random_int(18, 99),
            sex=fake.random_element(elements=('M', 'F')),

            n_inotropes_1_4h=fake.random_int(0, 3),
            had_rrt_1_4h=fake.random_element(elements=('false', 'true')),
            vent_type_1_4h=fake.random_element(
                elements=('Unknown', 'Room air', 'Oxygen', 'HFNO', 'Ventilated', 'CPAP')),

            note=fake.infection_status(),
        ))

    df = pd.DataFrame(referrals)
    return df


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
def gen_datatable_main(data_json):
    dfo = pd.DataFrame.from_records(data_json)
    dfo['organ_icons'] = ''

    llist = []
    # import pdb; pdb.set_trace()
    for t in dfo.itertuples(index=False):

        cvs = gen_cvs_icon(t.n_inotropes_1_4h)
        rs = gen_rs_icon(t.vent_type_1_4h)
        # import pdb; pdb.set_trace()
        aki = gen_aki_icon(t.had_rrt_1_4h)

        icon_string = f"{rs}{cvs}{aki}"
        ti = t._replace(organ_icons=icon_string)
        llist.append(ti)
    dfn = pd.DataFrame(llist, columns=dfo.columns)

    # Prep columns with ids and names
    COL_DICT = [
        {"name": v, "id": k} for k, v in conf.COLS.items() if k in conf.COLS_ABACUS
    ]
    # TODO: add in a method of sorting based on the order in config

    utils.deep_update(
        utils.get_dict_from_list(COL_DICT, "id", "organ_icons"),
        dict(presentation="markdown"),
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
            data=dfn.to_dict('records'),
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
            markdown_options={"html": True},
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


main_census_card = dbc.Container([
    dbc.Card([
        slider_census(),
        html.Div(id="abacus-datatable-main"),

    ]),

    html.Div([
        dcc.Interval(id="abacus-interval-data",
                     interval=conf.REFRESH_INTERVAL, n_intervals=0),
        dcc.Store(id="abacus-source-data"),
    ]),

])
