"""
For debugging
"""
from config.config import ConfigFactory
from dash import dash_table as dt
from dash import dcc, html
from wrangle import sitrep as wng

conf = ConfigFactory.factory()

DEBUG_ICU = "T03"

url_icu = wng.gen_hylode_url("sitrep", DEBUG_ICU)
df_sitrep = wng.get_hylode_data(url_icu, dev=conf.DEV_HYLODE)

url_census = wng.gen_hylode_url("census", DEBUG_ICU)
df_census = wng.get_hylode_data(url_census, dev=conf.DEV_HYLODE)

debug = html.Div(
    [
        html.P("Sitrep data only (before joining on to census data)"),
        html.Div(
            [
                "Trying out icons:",
                html.I(
                    className="flaticon-cough me-2",
                    # className="fas fa-ambulance me-2",
                    style={"font-size": "10rem", "color": "cornflowerblue"},
                ),
            ],
            className="d-flex align-items-center",
        ),
        dt.DataTable(
            id="debug",
            columns=[{"name": i, "id": i} for i in df_sitrep.columns],
            data=df_sitrep.to_dict("records"),
            filter_action="native",
            sort_action="native",
        ),
        html.P("Census data only (before joining on to sitrep data"),
        dt.DataTable(
            id="debug",
            columns=[{"name": i, "id": i} for i in df_census.columns],
            data=df_census.to_dict("records"),
            filter_action="native",
            sort_action="native",
        ),
    ]
)
