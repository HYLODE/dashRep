"""
PERRT page
Placeholder
"""
import dash_bootstrap_components as dbc
from config.config import ConfigFactory, footer, header, nav
from dash import dcc, html

from . import callbacks

conf = ConfigFactory.factory()

from dash import dash_table as dt
from dash import dcc, html

perrt_notes = dcc.Markdown(
"""
Each page acts as a place for the 'product owner' (in this case Dan) to try out their ideas

Broadly, we want to follow the principles of *here/there* and *now/next*

For PERRT, we might define our functional requirements to be

- a way of selecting the PERRT team (i.e. Tower, GWB, WMS)
- a list of deteriorating patients ordered by NEWS score
- some notion of how busy today is compared to recent history. An
  example might be a trend over time of the number of patients who have
  had a NEWS score greater than 4 in any 24h period? 

### April 2022

- list of patients
- time series of ICU admissions (displayed)
- time series of burden of work 
- aggregate model of demand
- first pass display of that model

### June 2022

- individual patient model
- conference abstract / draft paper


"""
)

main = dbc.Container(
    [
        # All content here organised as per bootstrap
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader(html.H2("PERTT placeholder")),
                        dbc.CardBody(html.Div([perrt_notes])),
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
            id="pertt-interval-data", interval=conf.REFRESH_INTERVAL, n_intervals=0
        ),
        # use this to source-data
        dcc.Store(id="pertt-source-data"),
    ]
)

# """Principal layout for PERRT page"""
perrt = dbc.Container(
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
