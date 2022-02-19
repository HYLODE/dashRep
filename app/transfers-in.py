# Simple single card version of the transfers in module
# Write as standalone here
# Then work out how to share data with other parts of the app separately
# Requirements
# Display an expandable datatable in card
# Store updates to that table 

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
    fake = Faker('en_GB')
    fake.add_provider(local_hospitals_provider)
    referrals = []
    for _ in range(n_rows):
        referrals.append(dict(
            name = fake.name(),
            hospital = fake.local_hospital()
        ))

    df = pd.DataFrame(referrals)
    return df


# @app.callback(
#     Output("dt_data", "data"),
#     Input("update_trigger", "n_intervals"),
#     )
# def load_data(n_intervals):
#     df = make_fake_df(2)
#     return df.to_dict("records")


@app.callback(
    Output("dt_table", "children"),
    Input("dt_data", "data"),
    )
def make_dt(data_json):
    df = pd.DataFrame.from_records(data_json)

    dtable = dt.DataTable(
        columns = [{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("records"),
        editable=True,
        row_deletable=True,
        )
    return dtable


@app.callback(
    Output('dt_data', 'data'),
    Input("update_trigger", "n_intervals"),
    Input('editing-rows-button', 'n_clicks'),
    State('dt_data', 'data'),
    # State('dt_data', 'columns'),
)
def add_row(n_intervals, n_clicks, rows):
    if n_clicks == 0:
        df = make_fake_df(2)
        return df.to_dict("records")
    if n_clicks > 0:
        rows.append({k: '' for k in rows[0].keys()})
        return rows


app.layout = dbc.Container([
    dbc.Card([
        # html.P('Hello world')
        html.Div(id='dt_table'),
        html.Button('Add Row', id='editing-rows-button', n_clicks=0),
        ]),

    html.Div([
        dcc.Interval(id="update_trigger", interval=conf.REFRESH_INTERVAL, n_intervals=0),
        dcc.Store(id='dt_data', storage_type='session'),
        ]),

])

if __name__ == '__main__':
    app.run_server(port=8010, host='0.0.0.0', debug=True)
