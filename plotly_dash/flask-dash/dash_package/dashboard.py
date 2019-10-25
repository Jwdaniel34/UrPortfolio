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
predictions = pd.read_csv('/Users/flatironschool/UrPortfolio/recommendation_system/rec_csvs/prediction_gv.csv')


app.layout = html.Div([
                # Configure navbar menu
        html.Div([
                html.H2(children = 'StockUp - A Fundamental Stock application For New Investors'),
                ], className = "banner"),

    dcc.Link('Investors Page', href='http://localhost:8501/'),
    dcc.Link(' | Recommender Page', href = 'http://localhost:8502'),
    # content will be rendered in this element
    html.Div(id='page-content'),

        html.Hr(),
        html.Div([
            html.H3('Technical Analysis'),
            html.H4('''   
       The technical analysis of stocks and trends attempts to predict future price movements,
         providing traders with the information needed to make a profit.Most technical analysis is focused 
         on determining whether or not a current trend will continue
          and, if not, when it will reverse.
            '''),
        ],style={'width': '49%', 'display': 'inline-block'}),
        
        html.Div(
            [html.H1("Compare Stocks Prices", style={'textAlign': 'center'}),
            dcc.Dropdown(id='my-dropdown',options= [{'label': i, 'value': j} for i,j in zip(comp,symbols)],
                multi=True,value=['A'],style={"display": "block","margin-left": "auto","margin-right": "auto","width": "40"}),
                dcc.Graph(id='my-graph')
                ], className="container"),
            
        html.Hr(),
        html.Div([
            html.H3('What Is a Sector?'),
            html.H4('''   
            A sector is an area of the economy in which businesses share the
            same or a related product or service. It can also be thought of as an
            industry or market that shares common operating characteristics. 
            Dividing an economy into different sectors allows for
            more in-depth analysis of the economy as a whole.
            '''),
        ],style={'width': '49%', 'display': 'inline-block'}),
        html.Div([
         html.Div([
                    dcc.Graph(
                            id = 'Sector Analysis',
                            figure = {
                                'data': [go.Pie(
                                    labels = ['Services','Financial','Technology','Consumer Goods','Industrial Goods',  
                                                 'Basic Materials','Healthcare','Utilities'] , values=values,
                                                 )],
                                'layout' : go.Layout(
                                title = 'Amount of Sectors in Dataset'),
                            })]),

                        html.Div([
                        dcc.Dropdown( id = 'sector fund',
                                    options = [{'label': 'Price', 'value': 'Price'}, {'label': 'Earnings', 'value': 'Earnings'},
                                                {'label': 'Dividend payout ratio', 'value': 'Dividend payout ratio'}],
                                    value ='Price'),
                                    html.Div(id='3')])
                                    ],style={'display': 'flex', 'justify-content': 'space-evenly'}),
                
                        html.Hr(),
                            html.Div([
                                html.H3('Analyze the Company'),
                                html.H4('''   
                                Fundamental analysis is the process of looking at a business at the most basic or fundamental financial level. 
                                This type of analysis examines the key ratios of a business to determine its financial health.
                                 Fundamental analysis can also give you an idea of the value of what a company's stock should be.
                                '''),
                            ],style={'width': '49%', 'display': 'inline-block'}),
                    html.Div([
                        dcc.Dropdown(
                                    id = 'stats', placeholder= 'Select a stock',
                                    options = [{'label': i, 'value': j} for i,j in zip(comp,symbols)],
                                    value ='A', style={'width': '49%', 'display': 'inline-block'}),
                                html.Div(id='1'),
                                html.Div(id='2'),
                                    ]),
                    # html.H1("Food Product Exports in the United States", style={"textAlign": "center"}),
                    # html.Div([html.Div([dcc.Dropdown(id='stock-selected1',
                    #                                  options=[{'label': i, 'value': j} for i,j in zip(comp,symbols)],
                    #                                  value="A")], className="six columns",
                    #                    style={"width": "40%", "float": "right"}),
                    #           html.Div([dcc.Dropdown(id='report-earnings2',
                    #                                  options=[{'label': 'Price', 'value': 'Price'}, {'label': 'Earnings', 'value': 'Earnings'},
                                                #               {'label': 'Dividend payout ratio', 'value': 'Dividend payout ratio'}],
                    #                                  value='Earnings')], className="six columns", style={"width": "40%", "float": "left"}),
                    #           ], className="row", style={"padding": 50, "width": "60%", "margin-left": "auto", "margin-right": "auto"}),
                    # dcc.Graph(id='new-graph'),                 
       
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
    prede = predictions[predictions['symbol'] == value]
    growth = prede['Growth'].sum()
    value = prede['Value'].sum()
    if growth > value:
        types = 'Growth'
        defin = "A growth stock is a stock of a company that generates substantial and sustainable positive cash flow and whose revenues and earnings are expected to increase at a faster rate than the average company within the same industry"
    else:
        types = 'Value'
        defin = 'A value stock is a stock that trades at a lower price relative to its fundamentals, such as dividends, earnings, or sales, making it appealing to value investors.'
    return html.Div([
                html.H1(f'Company - {company} ({asking})'),
                html.H2(f'Sector - {sector}'),
                html.H3(f'{asking} is considered a {types} stock'),
                html.H4(f'Definition : {defin}')
                ],style={'width': '49%', 'display': 'inline-block'})

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

# @app.callback(
#     dash.dependencies.Output('new-graph', 'figure'),
#     [dash.dependencies.Input('stock-selected1', 'value'),
#      dash.dependencies.Input('report-earnings2', 'value')])
# def update_graph(stock_selected1, report_earnings):
    # sectors_dyr = pd.DataFrame(companies.groupby(['sector','symbol','date','company'])[report_earnings].sum())
    # sectors_dyr = sectors_dyr.reset_index()
    # sectors_dyr.date = pd.to_datetime(sectors_dyr.date)
    # sectors_dyr.set_index("date", inplace=True)
    # symbol_1 = sectors_dyr[sectors_dyr['symbol'] == stock_selected1]
    # symbol_2 = sectors_dyr[sectors_dyr['symbol'] == stocks_selected2]

    # company_1 = symbol_1['company'].values[0]
    # company_2 = symbol_2['company'].values[0]
    # trace1 = []
    # for stock in stock_selected1:
    #     trace1.append(go.Scatter(x=stocks_df[stocks_df["stock"] == stock]["Date"],y=stocks_df[stocks_df["stock"] == stock]["Open"],mode='lines',
    #         opacity=0.7,name=f'Open {stock}',textposition='bottom center'))
    # trace2.append(go.Scatter(x = symbol_1.index, y = symbol_1[report_earnings], mode = 'lines+markers', name = f'{stock_selected1}'))
    # trace3.append(go.Scatter(x = symbol_2.index, y = symbol_2[report_earnings], mode = 'lines+markers', name = f'{stock_selected2}'))


@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    return html.Div([
        html.H3('You are on page {}'.format(pathname))
    ])

if __name__ == '__main__':
    app.run_server(port = 4050)