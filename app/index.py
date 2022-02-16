"""
Principle application file
https://dash.plotly.com/urls
"""
import logging
from dash import Input, Output, dcc, html

from config.config import ConfigFactory
from sitrep.layout import sitrep
from debug.debug import debug
from covid.covid import covid
from ed.ed import ed
from perrt.layout import perrt
from pacu.layout import pacu
from discharges.layout import discharges
from landing import landing
from abacus.layout import abacus

from app import app

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logging.basicConfig(level=logging.DEBUG)
logging.info('--- Application starting')

# configurable configuration
conf = ConfigFactory.factory()

app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)


@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def display_page(pathname):
    if pathname == "/sitrep":
        return sitrep
    elif pathname == "/covid":
        return covid
    elif pathname == "/ed":
        return ed
    elif pathname == "/perrt":
        return perrt
    elif pathname == "/pacu":
        return pacu
    elif pathname == "/discharges":
        return discharges
    elif pathname == "/debug":
        return debug
    elif pathname == "/":
        # Landing page will be served at the basic
        return landing
    elif pathname == "/abacus":
        return abacus
    else:
        # TODO return both the code and the page
        return "404"


if __name__ == "__main__":
    app.run_server(port=conf.SERVER_PORT, host=conf.SERVER_HOST, debug=True)
