import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

spacex_df = pd.read_csv('spacex_launch_dash.csv')
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

app = dash.Dash(__name__)

app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color':'black', 'font-size':40}),
                                html.Div(dcc.Dropdown(
                                    id='site-dropdown',
                                    value='ALL',
                                    options=[{'label': i, 'value':i} for i in spacex_df['Launch Site'].dropna().unique()] + 
                                    [{'label': 'All Sites', 'value': 'ALL'}],
                                    placeholder='Select a Launch Site here',
                                    searchable=True
                                    )
                                    ),
                                html.Br(),
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),
                                html.P("Payload Range(kg)"),
                                html.Div(dcc.Graph(id='success-payload-scatter-chart'))
                                ])


@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value')
              )
def get_pie_chart(entered_site):
    filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class', names='Launch Site', title='Total Successful Launch Count for all sites')
        return fig
    else:
        filtered_df['outcome'] = filtered_df['class'].map({1: 'Success', 0: 'Failure'})
        fig = px.pie(filtered_df, names='outcome', title=f'Success vs Failed Launch Counts for {entered_site} Site')
        return fig

if __name__ == '__main__':
    app.run()