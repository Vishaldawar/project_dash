import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

#app = dash.Dash(__name__)
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# ------------------------------------------------------------------------------
# Import and clean data (importing csv into pandas)
df = pd.read_csv("../data_sources/intro_bees.csv")

df = df.groupby(['State', 'ANSI', 'Affected by', 'Year', 'state_code'])[['Pct of Colonies Impacted']].mean()
df.reset_index(inplace=True)
print(df[:5])

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("Web Application Dashboards with Dash", style={'text-align': 'center','margin-top':20}),

    dcc.Dropdown(id="slct_year",
                 options=[
                     {"label": "2015", "value": 2015},
                     {"label": "2016", "value": 2016},
                     {"label": "2017", "value": 2017},
                     {"label": "2018", "value": 2018},
                     {"label": "2019", "value": 2019}],
                 multi=False,
                 value=2015,
                 style={'width': "40%", 'margin-left':40}
                 ),

    html.Div(id='output_container', children=[],style={'margin-left':70}),
    html.Br(),

    html.Div([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H3("Chloropleth Map", style={'text-align': 'center'}),
                    dcc.Graph(id='my_bee_map', figure={"layout" : {'height': 400,'width':550}})
                    ],style={'text-align':'center','margin-left':70})
                ], width=6),
            dbc.Col([
                html.Div([
                    html.H3("Bar Plot", style={'text-align': 'center'}),
                    dcc.Graph(id='scatter_map', figure={})
                ])
            ], width=6)
        ]),
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H3("Bar Plot two", style={'text-align': 'center'}),
                    dcc.Graph(id='my_bee_map_two', figure={})
                ])
            ], width=6),
            dbc.Col([
                html.Div([
                    html.H3("Chloropleth Map two", style={'text-align': 'center'}),
                    dcc.Graph(id='scatter_map_two', figure={"layout" : {'height': 400,'width':550}})
                ],style={'margin-left':70,'margin-right':30})
            ], width=6)
        ])
    ])
])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_bee_map', component_property='figure'),
     Output(component_id='scatter_map', component_property='figure'),
     Output(component_id='my_bee_map_two', component_property='figure'),
     Output(component_id='scatter_map_two', component_property='figure')],
    [Input(component_id='slct_year', component_property='value')]
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "The year chosen by user was: {}".format(option_slctd)

    dff = df.copy()
    dff = dff[dff["Year"] == option_slctd]
    dff = dff[dff["Affected by"] == "Varroa_mites"]

    fig = px.bar(dff, x='state_code', y='Pct of Colonies Impacted')

    # Plotly Express
    fig1 = px.choropleth(
        data_frame=dff,
        locationmode='USA-states',
        locations='state_code',
        scope="usa",
        color='Pct of Colonies Impacted',
        hover_data=['State', 'Pct of Colonies Impacted'],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        labels={'Pct of Colonies Impacted': '% of Bee Colonies'},
        template='plotly_dark'
    )

    # Plotly Graph Objects (GO)
    # fig = go.Figure(
    #     data=[go.Choropleth(
    #         locationmode='USA-states',
    #         locations=dff['state_code'],
    #         z=dff["Pct of Colonies Impacted"].astype(float),
    #         colorscale='Reds',
    #     )]
    # )
    #
    # fig.update_layout(
    #     title_text="Bees Affected by Mites in the USA",
    #     title_xanchor="center",
    #     title_font=dict(size=24),
    #     title_x=0.5,
    #     geo=dict(scope='usa'),
    # )

    return container, fig1, fig, fig, fig1


app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(host= '0.0.0.0',debug=True)
