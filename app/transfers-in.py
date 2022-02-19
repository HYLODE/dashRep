# Simple single card version of the transfers in module
# Write as standalone here
# Then work out how to share data with other parts of the app separately
# Requirements
# DONE: Display an expandable datatable in card
# TODO: Store updates to that table away from the page
# TODO: Add linked dynamic slider

import dash
import dash_bootstrap_components as dbc
import pandas as pd
from config.config import ConfigFactory
from dash import Dash, Input, Output, State
from dash import dash_table as dt
from dash import dcc, html

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
            hospital = fake.local_hospital(),
            accepted = fake.random_element(elements=('Yes', 'No')),
            note = f"{fake.name()} / {fake.infection_status()}",
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
        columns = [{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("records"),
        editable=True,
        row_deletable=True,
        )
    return dtable


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
    value = sum(df['accepted'].str[0].str.lower() == 'y')

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


app.layout = dbc.Container([
    dbc.Card([
        html.P('External referrals', className="card-title"),
        html.Div(id='div_slider'),
        html.Div(id='div_table'),
        dbc.Button('Add Row', id='editing-rows-button', n_clicks=0),
        ]),

    html.Div([
        dcc.Interval(id="update_trigger", interval=conf.REFRESH_INTERVAL, n_intervals=0),
        dcc.Store(id='store_dt_external', storage_type='session'),
        ]),

])

if __name__ == '__main__':
    app.run_server(port=8010, host='0.0.0.0', debug=True)
