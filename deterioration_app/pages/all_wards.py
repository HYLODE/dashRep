# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Input, Output, dash_table
import pandas as pd
import dash_bootstrap_components as dbc
import numpy as np

#Pull in the example data
df_unsorted = pd.read_csv('~/Documents/F4/Data_science/Deterioration/shap_living_sketch_df.csv')
df_unsorted = df_unsorted.iloc[:, 4:]
sorted_locs = np.argsort(-df_unsorted['Admission_probability'])
df = df_unsorted.loc[sorted_locs, :]

#Pull in the example inputs
input_data = pd.read_csv('~/Documents/F4/Data_science/Deterioration/morning_data_example_df.csv')
#Sort it by admission probability
input_data = input_data.loc[sorted_locs,:]

markdown_text = '''
# Interactive Deterioration App

This is an app to allow clinicians to interact with the list of who is deteriorating.
'''


app = Dash(__name__)

app.layout = html.Div(
    [
        #Title
        html.Div(
            html.H4(children='Deterioration App'), 
            style={'textAlign': 'center'}
        ),
        
        #html.Div(html.)
        
        #Options
        html.Div([
            html.Div(children=[
                html.Label('Number of Rows'),
                dcc.Dropdown([10, 20, 30, 40], 10, id = 'nrows'),

                html.Br(),
                html.Label('Wards to Include'),
                dcc.Dropdown([i for i in np.unique(df['ward_purpose'])],
                            [i for i in np.unique(df['ward_purpose'])],
                            id = 'dropdown',
                            multi=True),

                html.Br(),
                html.Label('Radio Items'),
                dcc.RadioItems(['New York City', 'Montréal', 'San Francisco'], 'Montréal'),
                ], 
            style={'padding': 10, 'flex': 1}),

            html.Div(children=[
                html.Label('Include Patients Not For Resus'),
                dcc.Checklist(['True'],
                            ['True'], id = 'dnacpr'
                ),

            html.Br(),
            
            #html.Label('Text Input'),
            
            #dcc.Input(value='MTL', type='text'),

            html.Br(),
            html.Label('Number of SHAP Features'),
            dcc.Slider(
                id='slider-input',
                min=0,
                max=len(df.columns),
                marks={i: f'{i}' if i == 1 else str(i) for i in range(6)},
                value=5,
            ),
            ], 
            style={'padding': 10, 'flex': 1})
            
        ], 
    
        style={'display': 'flex', 'flex-direction': 'row'}        
        ),
        
        #Table
        html.Div(id = 'my-output'), 
        
        #Table
        #html.Div(id = 'states_out'), 
        
    ]
)

@app.callback(
    Output(component_id='my-output', component_property='children'),
    Input(component_id='slider-input', component_property='value'), 
    Input(component_id = 'dropdown', component_property = 'value'),
    Input(component_id = 'nrows', component_property = 'value'),
    Input(component_id = 'dnacpr', component_property = 'value')
)
def generate_table(ncols, search_value, max_rows, dnacpr):
    
    #Include patients not for resus
    if not dnacpr:
        df0 = df.loc[df['dnacpr'] != 'DNACPR', :]
        input_data0 = input_data.loc[df['dnacpr'] != 'DNACPR', :] 
    else:
        df0 = df
        input_data0 = input_data
    
    #Chose only certain wards
    ward_index = [i for i, j in enumerate(df0['ward_purpose']) if j in search_value]
    df1 = df0.iloc[ward_index, :]
    
    global input_data1
    input_data1 = input_data0.iloc[ward_index, :]
    
    global dff
    dff = df1.iloc[:max_rows, :(8 + ncols)]
    
    return dbc.Container([
            dbc.Label('Click a cell in the table:'),
            dash_table.DataTable(dff.to_dict('records'),[{"name": i, "id": i} for i in dff.columns], id='tbl'),
            dbc.Alert(id='tbl_out'),
    ])
    

@app.callback(Output('tbl_out', 'children'), 
              Input('tbl', 'active_cell'))
def update_graphs(active_cell):
    
    #return dff.loc[active_cell['row'], active_cell['column_id']] if active_cell else "Click the table"
    if active_cell:
        if active_cell['column'] > 7:
            
            #Pull what's in the box
            location = dff.iloc[active_cell['row'], active_cell['column']]
            return input_data1.loc[active_cell['row'], location]
            
        else:
            return dff.loc[active_cell['row'], active_cell['column_id']] 
    else:
        return 'Click the table'

if __name__ == '__main__':
    app.run_server(debug=True)
    
#Think about putting the last 12 hours of observations underneath for when you click on a given patient? And or some additional information about them?