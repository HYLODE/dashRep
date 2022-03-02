# Simple single card version of the main census module
# Write as standalone here
#
# Requirements
# TODO: simple datatable of the basic census info
# TODO: loop through table and construct string for markdown
# TODO: recognise when the table is updated and maintain state
#       break this down
#       - [ ] display alert when table changes

import arrow
import dash
import dash_bootstrap_components as dbc
import pandas as pd

from config.config import ConfigFactory

from dash_extensions.enrich import Input
from dash_extensions.enrich import Output
from dash_extensions.enrich import ServersideOutput
from dash_extensions.enrich import State

from dash import dash_table as dt
from dash import dcc
from dash import html


conf = ConfigFactory.factory()


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
    ServersideOutput("store_dt_external", "data"),
    Input("update_trigger", "n_intervals"),
    State("store_dt_external", "data"),
)
def load_data(n_intervals, dt_external):
    print('refreshing page b/c update trigger time interval has elapsed')
    if dt_external is None:
        df = make_fake_df(2)
        return df.to_dict("records")
    else:
        return dt_external


@app.callback(
    Output("div_table", "children"),
    Input("store_dt_external", "modified_timestamp"),
    State("store_dt_external", "data"),
)
def gen_datatable_main(modified_ts, data_json):
    dfo = pd.DataFrame.from_records(data_json)

    # Prep columns with ids and names
    COL_DICT = [
        {"name": v, "id": k} for k, v in conf.COLS.items() if k in conf.COLS_ABACUS
    ]

    DISCHARGE_OPTIONS = ["Ready", "No", "Review"]

    dto = (
        dt.DataTable(
            id="dt-tbl-main",
            columns=COL_DICT,
            data=dfo.to_dict('records'),
            editable=True,
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
    Output("modified_msg", "children"),
    Input("dt_update_trigger", "n_intervals"),
)
def display_modified_msg(n_intervals):

    if n_intervals:
        ts_string = arrow.utcnow().shift(seconds=-1 * n_intervals).humanize()
        res = f"Data modified {ts_string}"
        alert = dbc.Alert(res, color="warning")
    else:
        ts_string = arrow.utcnow().format('YYYY-MM-DD HH:mm:ss')
        res = f"Data loaded at {ts_string}"
        alert = dbc.Alert(res, color="success")

    buttons = dbc.Button("Primary", color="primary", className="me-1")

    return dbc.Col([alert, buttons])

@app.callback(
    Output("dt_update_trigger", "disabled"),
    Input("dt-tbl-main", "data_timestamp"),
    State("dt_update_trigger", "disabled"),
)
def start_dt_update_trigger(dt_ts, dt_update_boolean):
    if dt_ts:
        return False
    else:
        return True


@app.callback(
    Output("store_dt_local", "data"),
    Input("dt-tbl-main", "data_timestamp"),
    State("dt-tbl-main", "data"),
)
def update_data(dt_ts, dt_now):
    return dt_now


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
        html.Div(id='div_table'),
    ]),


])

try_two = dbc.Container([
    dbc.Card([
        html.P('Try Two', className="card-title"),
    ]),

])


app_stores = html.Div([
    dcc.Interval(id="update_trigger",
                 interval=conf.REFRESH_INTERVAL, n_intervals=0),
    dcc.Interval(id="dt_update_trigger",
                 interval=1000, n_intervals=0, disabled=True),
    dcc.Store(id='store_dt_external', storage_type='session'),
    dcc.Store(id='store_dt_local', storage_type='session'),
])


header = dbc.Container(
    dbc.Row(
        [
            dbc.Col(
                [
                    dbc.NavbarSimple(
                        children=[
                            dbc.NavItem(dbc.NavLink("HOME", href="/")),
                            dbc.NavItem(dbc.NavLink(
                                "TRY_TWO", href="/try_two")),
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

alert_modified = dbc.Row(
    dbc.Col([
    html.Div(id='modified_msg')
        ])
)

app.layout = html.Div(
    [
        app_stores,
        header,
        alert_modified,
        dcc.Location(id="url", refresh=False), html.Div(id="page-content")
    ]
)

if __name__ == '__main__':
    app.run_server(port=8010, host='0.0.0.0', debug=True)
