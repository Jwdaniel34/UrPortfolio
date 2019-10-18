import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import dash
import glob
from dash_package import app
from dash_package.functions import *
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output, State
import chart_studio

companies = pd.read_csv('/Users/flatironschool/UrPortfolio/csv_files/companies.csv')
companies = companies.rename(columns={"Quarter end": "date"})
predictions = pd.read_csv('/Users/flatironschool/UrPortfolio/recommendation_system/rec_csvs/prediction_gv.csv')
symbols = companies['symbol'].unique()
symbols = symbols.tolist()
comp = companies['company'].unique()
comp = comp.tolist()
values = companies['sector'].value_counts(normalize = False)


# app = dash.Dash()
# app.config.suppress_callback_exceptions = True

app.layout = html.Div([
            
        html.Div([
                html.H2(children = 'UrStockPortfolio'),
                html.Img(src="static/stock_icons.png"),
                ], className = "banner",),

         html.Div([
             html.H3(children = "A fundamental Stock application For New Investors"),
                    dcc.Graph(
                            id = 'Sector Analysis',
                            figure = {
                                'data': [go.Pie(
                                    labels = ['Services','Financial','Technology','Consumer Goods','Industrial Goods',  
                                                'Basic Materials','Healthcare','Utilities'] , 
                                    values=values)
                                ],
                                'layout' : go.Layout(
                                title = 'Amount of Sectors in Dataset',
                                legend=dict(x=0,y=1.0),)
                            })],style={'width': '49%', 'display': 'inline-block'}),
    
                            html.Div([
                            dcc.Dropdown(
                                        id = 'stats',
                                        options = [{'label': i, 'value': j} for i,j in zip(comp,symbols)],
                                        value ='', style={'width': '49%', 'display': 'inline-block'}),
                                    html.Div(id='1'),
                                        ]),
                            
                                                                
       
])

app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

@app.callback(Output('1', 'children'), 
              [Input('stats', 'value')])                           
def pe_ratio(value):
    if value is None:
    # PreventUpdate prevents ALL outputs updating
        raise dash.exceptions.PreventUpdate
    test = companies[companies['symbol'] == value]
    asking = value.upper()
    company = test['company'].values[0]
    sector = test['sector'].values[0]
    labels_gv = ['Growth', 'Value']
    values_gv = test['growth'].value_counts()
    data= [go.Pie(labels=labels_gv, values=values_gv, hole=.3, 
                  name= f'{asking}', hoverinfo="label+percent+name")]

    labels_roa = ['Growth', 'No Growth']
    values_roa = test['growth_roa'].value_counts()
    data_1= [go.Pie(labels=labels_roa, values=values_roa, hole=.3,
                    name= f'{asking}', hoverinfo="label+percent+name")]

    labels_roe = ['Growth', 'No Growth']
    values_roe = test['growth_roe'].value_counts()
    data_2 = [go.Pie(labels=labels_roe, values=values_roe, hole=.3, name= f'{asking}')]

    return html.Div([
                html.Div([
                    html.H2(f'{company}'),
                    html.H3(f'{sector} Sector'),
                    dcc.Graph(
                    id='pe_ratio',
                    figure={
                            'data': data,
                            'layout': go.Layout(title=f'Growth - {asking} Stock P/E ratio',
                            legend=dict(x=0,y=1.0),
                            )})],className="six columns"),
                html.Div([
                    dcc.Graph(
                        id='roa', 
                        figure = {'data': data_1, 
                                'layout': go.Layout(title= f"Growth Return on Assest - {asking} ",
                                                        legend=dict(x=0,y=1.0),
                                                        )}),
                        html.H4( "PE Ration")],className="six columns"), 
                html.Div([
                    dcc.Graph(id='roe', 
                            figure = {'data': data_2, 
                                    'layout': go.Layout(title= f"Growth Return on Equity - {asking}",
                                                legend=dict(x=0,y=1.0),
                                                )})],className="six columns"),
                                                ],style={'width': '49%', 'display': 'inline-block'})
                


if __name__ == '__main__':
    app.run_server(port = 4050)