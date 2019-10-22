import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import pandas_datareader.data as web
from iexfinance.stocks import get_historical_data
import numpy as np
import datetime
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
stocks_df = pd.read_csv('/Users/flatironschool/UrPortfolio/dash_setup/dash_timeseries.csv')
stocks_df = stocks_df.drop('Unnamed: 0', axis = 1)
stocks_df['Date'] = pd.to_datetime(stocks_df.Date, infer_datetime_format=True)
# stocks_df['year'] = pd.DatetimeIndex(stocks_df['date']).year


app.layout = html.Div([
        
        dbc.NavbarSimple(
                    children=[
                    dbc.NavItem(dbc.NavLink("Page 1", href="#")),
                    dbc.DropdownMenu(children=[
                    dbc.DropdownMenuItem("Page 2", href="#"),
                                ],nav=True,
                            in_navbar=True,),
                    ],
                    brand="NavbarSimple",
                    brand_href="#",
                    color="primary",
                    dark=True,
                ),
                # Configure navbar menu
        # html.Div([
        #         html.H2(children = 'UrStockPortfolio'),
        #         ], className = "banner"),

        html.H3('A Fundamental Stock application For New Investors'),

        html.Div(
            [html.H1("Compare Stock Prices", style={'textAlign': 'center'}),
            dcc.Dropdown(id='my-dropdown',options= [{'label': i, 'value': j} for i,j in zip(comp,symbols)],
                multi=True,value=['A'],style={"display": "block","margin-left": "auto","margin-right": "auto","width": "40"}),
                dcc.Graph(id='my-graph')
                ], className="container"),
            
        html.Hr(),

        html.H4(children = "Fundamental Analysis on Sectors"),
         html.Div([
                    html.Div([
                    dcc.Graph(
                            id = 'Sector Analysis',
                            figure = {
                                'data': [go.Pie(
                                    labels = ['Services','Financial','Technology','Consumer Goods','Industrial Goods',  
                                                'Basic Materials','Healthcare','Utilities'] , values=values)],
                                'layout' : go.Layout(
                                title = 'Amount of Sectors in Dataset'),
                            })]),

                        html.Div([
                        dcc.Dropdown( id = 'sector fund',
                                    options = [{'label': 'Price', 'value': 'Price'}, {'label': 'Earnings', 'value': 'Earnings'}],
                                    value ='Price'),
                                    html.Div(id='3')])
                                    ],style={'display': 'flex', 'justify-content': 'space-evenly'}),
                
                html.Hr(),

            html.Div([
                    dcc.Dropdown(
                                id = 'stats', placeholder= 'Select a stock',
                                options = [{'label': i, 'value': j} for i,j in zip(comp,symbols)],
                                value ='A', style={'width': '49%', 'display': 'inline-block'}),
                            html.Div(id='1'),
                            html.Div(id='2'),
                                ]),
                            
                                                                
       
])


@app.callback(Output('my-graph', 'figure'),
              [Input('my-dropdown', 'value')])
def update_graph(selected_dropdown_value):
    dropdown = [{'label': j, 'value': i} for j,i in zip(comp,symbols)]
    trace1 = []
    trace2 = []
    for stock in selected_dropdown_value:
        trace1.append(go.Scatter(x=stocks_df[stocks_df["stock"] == stock]["Date"],y=stocks_df[stocks_df["stock"] == stock]["Open"],mode='lines',
            opacity=0.7,name=f'Open {stock}',textposition='bottom center'))
        trace2.append(go.Scatter(x=stocks_df[stocks_df["stock"] == stock]["Date"],y=stocks_df[stocks_df["stock"] == stock]["Close"],mode='lines',
            opacity=0.6,name=f'Close {stock}',textposition='bottom center'))
    traces = [trace1, trace2]
    data = [val for sublist in traces for val in sublist]
    figure = {'data': data,
        'layout': go.Layout(colorway=["#5E0DAC", '#FF4F00', '#375CB1', '#FF7400', '#FFF400', '#FF0056'],
            height=600,title=f"Opening and Closing Prices for Stocks Over Time",
            xaxis={"title":"Date",
                   'rangeselector': {'buttons': list([{'count': 1, 'label': '1M', 'step': 'month', 'stepmode': 'backward'},
                                                      {'count': 6, 'label': '6M', 'step': 'month', 'stepmode': 'backward'},
                                                      {'step': 'all'}])},
                   'rangeslider': {'visible': True}, 'type': 'date'},yaxis={"title":"Price (USD)"})}
    return figure

@app.callback(Output('3', 'children'),
            [Input('sector fund', 'value')])
def sectors(value):
    sectors_growth = pd.DataFrame(companies.groupby(['sector','growth'])[value].sum())
    sectors_growth = sectors_growth.reset_index()
    value_stocks = sectors_growth[sectors_growth['growth'] == 0]
    growth_stocks = sectors_growth[sectors_growth['growth'] == 1]
    value_stocks = value_stocks.rename({'growth': 'value'}, axis =1 )
    label = value_stocks['sector']
    values = value_stocks[value]
    growing = growth_stocks[value]
    trace1 = go.Bar(x=label,y= growing,name='Growth Stock', marker_color='rgb(55, 83, 109)')
    trace2 = go.Bar(x=label, y=values,name='Value Stock',marker_color='rgb(26, 118, 255)')
    data = [trace1, trace2]

    return html.Div([
                dcc.Graph(
                figure = {'data':data,
                'layout': go.Layout(title='Industry Growth and Value Stocks',
                                    colorway=["#EF963B", "#EF533B"], hovermode="closest",
                                    xaxis={'title': "Sector", 'titlefont': {'color': 'black', 'size': 14},
                                        'tickfont': {'size': 10, 'color': 'black'}},
                                    yaxis={'title': f"Stock {value} (million USD)", 'titlefont': {'color': 'black', 'size': 14, },
                                        'tickfont': {'color': 'black'}
                                        })})], style={'width': '700px', 'display': 'inline-block'})


@app.callback(Output('1', 'children'),
            [Input('stats', 'value')])
def company(value):
    test = companies[companies['symbol'] == value]
    asking = value.upper()
    sector = test['sector'].iloc[0]
    company = test['company'].iloc[0]
    return html.Div([
                html.H2(f'{company}'),
                html.H3(f'{sector}')
                ])

@app.callback(Output('2', 'children'), 
              [Input('stats', 'value')])                           
def pe_ratio(value):
    if value is None:
    # PreventUpdate prevents ALL outputs updating
        raise dash.exceptions.PreventUpdate
    test = companies[companies['symbol'] == value]
    asking = value.upper()
    sector = test.iloc[0][2]
    company = test['company'].iloc[0]
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
                    dcc.Graph(
                    # id='pe_ratio',
                    figure={
                            'data': data,
                            'layout': go.Layout(title=f'Growth Price to Earning Ratio - {asking} Stock',
                            
                            )})],className="six columns", style={'max-width': '500px'}),
                html.Div([
                    dcc.Graph(
                        # id='roa', 
                        figure = {'data': data_1, 
                                'layout': go.Layout(title= f"Growth Return on Assest - {asking} ",
                                                        
                                                        )}),
                        ],className="six columns", style={'max-width': '500px'}), 

                html.Div([
                    dcc.Graph(
                            # id='roe', 
                            figure = {'data': data_2, 
                                    'layout': go.Layout(title= f"Growth Return on Equity - {asking}",
                                                
                                                )})],className="six columns", style={'max-width': '500px'}),
                                                ],style={'display': 'flex', 'justify-content': 'center'})
                


if __name__ == '__main__':
    app.run_server(port = 4050)