# Simple single card version of the main census module
# Write as standalone here
#
# Requirements
# TODO: simple datatable of the basic census info
# TODO: loop through table and construct string for markdown

import dash
import dash_bootstrap_components as dbc
import pandas as pd

from config.config import ConfigFactory
from dash import Dash
from dash import Input
from dash import Output
from dash import State
from dash import dash_table as dt
from dash import dcc
from dash import html

from utils import utils

conf = ConfigFactory.factory()

COLOUR_GREY = "#c0c0c077"
COLOUR_GREEN = "#008000ff"
COLOUR_AMBER = "#ffa500ff"
COLOUR_RED = "#ff0000ff"

app = dash.Dash(
    __name__,
    title="Testing",
    update_title=None,
    external_stylesheets=[
        dbc.themes.YETI,
        dbc.icons.FONT_AWESOME,
    ],
    suppress_callback_exceptions=True,
)



def gen_aki_icon(level: str) -> str:
    icon = 'fa fa-flask'
    level = level.lower()
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
    level = level.lower()
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
    n = int(level)
    if n == 0:
        colour = COLOUR_GREY
    elif n == 1:
        colour = COLOUR_AMBER
    else:
        colour = COLOUR_RED
    icon_string = f'<i class="{icon}" style="color: {colour};"></i>'
    return icon_string


# {
#     "name": "Joseph Valdez",
#     "admission_age_years": 110,
#     "sex": "M",

#     "n_inotropes_1_4h": 0,
#     "had_rrt_1_4h": false,
#     "vent_type_1_4h": "Unknown",

#     "episode_slice_id": 162117,
#     "csn": "1048246392",
#     "admission_dt": "2021-10-07T19:30:00+01:00",
#     "elapsed_los_td": 973800,
#     "bed_code": "BY01-12",
#     "bay_code": "BY01",
#     "bay_type": "Regular",
#     "ward_code": "T03",
#     "mrn": "42636453",
#     "dob": "1911-07-23",
#     "admission_age_years": 110,
#     "sex": "M",
#     "is_proned_1_4h": false,
#     "discharge_ready_1_4h": "No",
#     "is_agitated_1_8h": false,
#     "had_nitric_1_8h": false,
#     "had_trache_1_12h": false,
#     "avg_heart_rate_1_24h": null,
#     "max_temp_1_12h": null,
#     "avg_resp_rate_1_24h": null,
#     "wim_1": 0
# },

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
    Output("store_dt_external", "data"),
    Input("update_trigger", "n_intervals"),
)
def load_data(n_intervals):
    df = make_fake_df(2)
    return df.to_dict("records")


@app.callback(
    Output("div_table", "children"),
    Input("store_dt_external", "data"),
)
def make_dt(data_json):
    df = pd.DataFrame.from_records(data_json)

    dtable = dt.DataTable(
        id="dt_table",
        data=df.to_dict("records"),
        columns=[{"name": i, "id": i} for i in df.columns],
        editable=True,
        row_deletable=True,
        # 2022-02-19 persistence args don't seem to affect forced refresh
        # persistence=True,
        # persisted_props=['data'],
        # persistence_type='session',
    )
    return dtable


@app.callback(
    Output("div_table_icons", "children"),
    Input("store_dt_external", "data"),
)
def gen_datatable_main(data_json):
    dfo = pd.DataFrame.from_records(data_json)
    dfo['organ_icons'] = ''

    llist = []
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

    # dtable = dt.DataTable(
    #     id="dt_table",
    #     data=dfn.to_dict("records"),
    #     columns=columns,
    #     editable=True,
    #     row_deletable=True,
    #     markdown_options={"html": True},
    # )
    # return dtable

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


@app.callback(
    Output('dt_table', 'data'),
    Input('editing-rows-button', 'n_clicks'),
    State('dt_table', 'data'),
    State('dt_table', 'columns'),
)
def add_row(n_clicks, rows, columns):
    rows.append({c['id']: '' for c in columns})
    return rows


@app.callback(
    Output("div_slider", "children"),
    Input("dt_table", "data"),
)
def make_slider(data_json):
    df = pd.DataFrame.from_records(data_json)
    _max = df.shape[0]
    value = _max

    marks = {str(i): str(i) for i in range(0, _max + 1)}
    slider = dcc.Slider(
        id="dt_slider",
        min=0,
        max=_max,
        value=value,
        marks=marks,
        step=1,  # i.e. patients are integers
        updatemode="drag",
        tooltip={"placement": "top", "always_visible": True},
    )

    return slider

@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def display_page(pathname):
    if pathname == "/":
        return try_one
    elif pathname == "/try_two":
        return try_two
    else:
        # TODO return both the code and the page
        return "404"


try_one = dbc.Container([
    dbc.Card([
        html.P('Try One', className="card-title"),
        html.Div(id='div_slider'),
        html.P('Original table', className="card-body"),
        html.Div(id='div_table'),
        html.P('Icon table', className="card-body"),
        html.Div(id='div_table_icons'),
        dbc.Button('Add Row', id='editing-rows-button', n_clicks=0),
    ]),

    html.Div([
        dcc.Interval(id="update_trigger",
                     interval=conf.REFRESH_INTERVAL, n_intervals=0),
        dcc.Store(id='store_dt_external', storage_type='session'),
    ]),

])

try_two = dbc.Container([
    dbc.Card([
        html.P('Try Two', className="card-title"),
    ]),

])


header = dbc.Container(
    dbc.Row(
        [
            # dbc.Col([
            #             html.I(className="fa fa-lungs-virus"),
            #             ], md=1),
            dbc.Col(
                [
                    dbc.NavbarSimple(
                        children=[
                            dbc.NavItem(dbc.NavLink("HOME", href="/")),
                            dbc.NavItem(dbc.NavLink("TRY_TWO", href="/try_two")),
                        ],
                        brand="UCLH Critical Care Sitrep",
                        brand_href="/",
                        brand_external_link=True,
                        color="primary",
                        dark=True,
                        sticky=True,
                    ),
                ]
            ),
        ]
    ),
    fluid=True,
)

app.layout = html.Div(
    [
    header,
    dcc.Location(id="url", refresh=False), html.Div(id="page-content")
    ]
)

if __name__ == '__main__':
    app.run_server(port=8010, host='0.0.0.0', debug=True)
