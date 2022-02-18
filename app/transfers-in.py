# Simple single card version of the transfers in module
# Write as standalone here
# Then work out how to share data with other parts of the app separately
# Requirements
# Display an expandable datatable in card
# Store updates to that table 

import pandas as pd
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


print(make_fake_df(2))






app.layout = html.Div("hello world" )

if __name__ == '__main__':
    app.run_server(port=8010, host='0.0.0.0', debug=True)
