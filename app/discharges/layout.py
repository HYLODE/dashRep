"""
Discharges page
Placeholder
"""
import dash_bootstrap_components as dbc
from config.config import ConfigFactory, footer, header, nav
from dash import dcc, html

from . import callbacks

conf = ConfigFactory.factory()

from dash import dash_table as dt
from dash import dcc, html

pacu_notes = dcc.Markdown(
"""
Each page acts as a place for the 'product owner' (in this case ???) to try out their ideas

Broadly, we want to follow the principles of *here/there* and *now/next*

For DISCHARGES, we might define our functional requirements to be ...

The first few are intended just to report on 'now' and don't do any modelling

- a report of the common downstream wards from critical care
- how busy are the common downstream wards for critical care

### ?? 2022

- list of wards / flows out from critical care
- list of current inpatients on those wards

### TBC 2022

- discharge readiness status for each patient on those wards
- LoS model running for each of those wards


"""
)

main = dbc.Container(
    [
        # All content here organised as per bootstrap
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader(html.H2("Discharges placeholder")),
                        dbc.CardBody(html.Div([pacu_notes])),
                    ],
                ),
                md=12,
            ),
        ),
    ],
    fluid=True,
)

# use this to store dash components that you don't need to 'see'
dash_stores = html.Div(
    [
        # update and refresh
        dcc.Interval(
            id="discharges-interval-data", interval=conf.REFRESH_INTERVAL, n_intervals=0
        ),
        # use this to source-data
        dcc.Store(id="discharges-source-data"),
    ]
)

# """Principal layout for discharges page"""
discharges = dbc.Container(
    fluid=True,
    className="dbc",
    children=[
        header,
        nav,
        main,
        footer,
        dash_stores,
    ],
)
