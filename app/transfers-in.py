# Simple single card version of the transfers in module
# Write as standalone here
# Then work out how to share data with other parts of the app separately
# Requirements
# Display an expandable datatable in card
# Store updates to that table 

import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

from config.config import ConfigFactory

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

app.layout = html.Div("hello world" )

if __name__ == '__main__':
    app.run_server(port=8010, host='0.0.0.0', debug=True)
