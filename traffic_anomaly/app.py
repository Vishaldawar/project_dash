import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from data_create import short_names, data
import datetime

#app = dash.Dash(__name__)
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# ------------------------------------------------------------------------------
# Import and clean data (importing csv into pandas)
df = pd.read_csv("./data_sources/traffic_data.csv",index_col=0)
print(df.index.dtype)
print(df[:5])

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("CIBIL Anomaly Detection", style={'text-align': 'center','margin-top':20}),

    dcc.Dropdown(id="bank",
                 options=[{"label" : data[bank], "value" : bank} for bank in short_names],
                 multi=False,
                 value=short_names[0],
                 style={'width': "40%", 'margin-left':40}
                 ),

    html.Div(id='output_container', children=[],style={'margin-left':80, 'margin-top':20}),
    html.Br(),

    html.Div([
                html.H3("Traffic Anomaly Dashboard", style={'text-align': 'center'}),
                dcc.Graph(id='bank_traffic', figure={})
        ])
])

# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='bank_traffic', component_property='figure')],
    [Input(component_id='bank', component_property='value')]
)

def update_graph(bank):
    print(bank)
    print(type(bank))

    container = "The bank chosen by user was: {}".format(data[bank])
    dff = df.copy()
    time = '2019-05-29'
    dff = dff[dff.index >= time]

    fig = px.line(dff, x=dff.index, y=bank)

    return container, fig

app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
