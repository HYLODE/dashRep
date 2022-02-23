# Simple single card version of the transfers in module
# Write as standalone here
# Then work out how to share data with other parts of the app separately
# Requirements
# DONE: Display an expandable datatable in card
# DONE: Add linked dynamic slider
# TODO: Store updates to that table away from the page
#       work with dt properties to first define if the data has changed
#       data_previous as input trigger to know if the data has changed

from app import app
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

conf = ConfigFactory.factory()

# app = dash.Dash(
#     __name__,
#     title="Testing",
#     update_title=None,
#     external_stylesheets=[
#         dbc.themes.YETI,
#         dbc.icons.FONT_AWESOME,
#     ],
#     suppress_callback_exceptions=True,
# )


def make_fake_df(n_rows):
    # run the imports here since this function won't be needed in production
    from faker import Faker
    from faker.providers import DynamicProvider
    local_hospitals_provider = DynamicProvider(
        provider_name="local_hospital",
        elements=['Royal Free', 'Whittington', 'North Middlesex', 'Barnet']
    )
    infection_status_provider = DynamicProvider(
        provider_name="infection_status",
        elements=['clean', 'COVID', 'ESBL', '']
    )
    fake = Faker('en_GB')
    fake.add_provider(local_hospitals_provider)
    fake.add_provider(infection_status_provider)
    referrals = []
    for _ in range(n_rows):
        referrals.append(dict(
            hospital=fake.local_hospital(),
            accepted=fake.random_element(elements=('Yes', 'No')),
            note=f"{fake.name()} / {fake.infection_status()}",
        ))

    df = pd.DataFrame(referrals)
    return df


@app.callback(
    Output("tin_store_dt", "data"),
    Input("tin_update_trigger", "n_intervals"),
)
def load_data(n_intervals):
    df = make_fake_df(2)
    return df.to_dict("records")


@app.callback(
    Output("tin_div_table", "children"),
    Input("tin_store_dt", "data"),
)
def make_dt(data_json):
    df = pd.DataFrame.from_records(data_json)

    dtable = dt.DataTable(
        id="tin_dt_table",
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("records"),
        editable=True,
        row_deletable=True,
        # style_data={
        #     'whiteSpace': 'normal',
        #     'height': 'auto',
        #     'lineHeight': '15px',
        # },

        style_cell={
            "fontSize": 11,
            'font-family': 'sans-serif',
            "padding": "1px",
            'lineHeight': '15px',
        },
        style_cell_conditional=[
            {'if': {'column_id': 'accepted'},
             'width': '15%'},
            {'if': {'column_id': 'hospital'},
             'width': '25%'},
        ],
        style_data={
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
            'maxWidth': 0
        },
        tooltip_data=[
            {
                column: {'value': str(value), 'type': 'markdown'}
                for column, value in row.items()
            } for row in df.to_dict('records')
        ],
        tooltip_duration=None,

        # 2022-02-19 persistence args don't seem to affect forced refresh
        # but I think this is b/c the data changes each time b/c your generating fresh data
        persistence=True,
        persisted_props=['data'],
        # persistence_type='session',
    )
    return dtable


@ app.callback(
    Output('tin_dt_table', 'data'),
    Input('tin_rows_button', 'n_clicks'),
    State('tin_dt_table', 'data'),
    State('tin_dt_table', 'columns'),


)
def add_row(n_clicks, rows, columns):
    rows.append({c['id']: '' for c in columns})
    return rows


@ app.callback(
    Output("tin_div_slider", "children"),
    Input("tin_dt_table", "data"),
)
def make_slider(data_json):
    df = pd.DataFrame.from_records(data_json)
    _max = df.shape[0]
    try:
        value = sum(df['accepted'].str[0].str.lower() == 'y')
    except AttributeError:
        value = 0

    marks = {str(i): str(i) for i in range(0, _max + 1)}
    slider = dcc.Slider(
        id="plus_transfers",
        min=0,
        max=_max,
        value=value,
        marks=marks,
        step=1,  # i.e. patients are integers
        updatemode="drag",
        tooltip={"placement": "top", "always_visible": True},
    )

    return slider


# app.layout = dbc.Container([
transfers_in_card = dbc.Container([
    dbc.Card([
        html.P('External referrals', className="card-title"),
        html.Div(id='tin_div_slider'),
        html.Div(id='tin_div_table'),
        dbc.Button('Add Row', id='tin_rows_button', n_clicks=0),
    ]),

    html.Div([
        dcc.Interval(id="tin_update_trigger",
                     interval=conf.REFRESH_INTERVAL, n_intervals=0),
        dcc.Store(id='tin_store_dt', storage_type='session'),
    ]),

])

# if __name__ == '__main__':
#     app.run_server(port=8010, host='0.0.0.0', debug=True)
