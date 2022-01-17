"""
PACU page
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
Each page acts as a place for the 'product owner' (in this case Jen) to try out their ideas

Broadly, we want to follow the principles of *here/there* and *now/next*

For PACU, we might define our functional requirements to be

The first few are intended just to report on 'now' and don't do any modelling

- a way of selecting the PACU area (i.e. Tower, GWB, WMS)
- a list of surgical patients planned for the next 7 days? excluding day
  surgery with a flag indicating if PACU is requested
- some notion of how busy today is compared to recent history. An
  example might be a trend over time of the number of patients booked
  for surgery and another line for the number of patients booked for
  PACU

### April 2022

- list of patients
- time series of burden of work 

### TBC 2022

- modelling inputs
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
                        dbc.CardHeader(html.H2("PACU placeholder")),
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
            id="pacu-interval-data", interval=conf.REFRESH_INTERVAL, n_intervals=0
        ),
        # use this to source-data
        dcc.Store(id="pacu-source-data"),
    ]
)

# """Principal layout for pacu page"""
pacu = dbc.Container(
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
