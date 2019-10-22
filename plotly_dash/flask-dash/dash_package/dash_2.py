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

cluster_rec = pd.read_csv('rec_csvs/clusters_rec.csv')
growth_stocks = pd.read_csv('rec_csvs/growth_stocks.csv')
value_stocks = pd.read_csv('rec_csvs/value_stocks.csv')
predictions = pd.read_csv('rec_csvs/prediction_gv.csv')
growth_stocks = growth_stocks.rename({'0':'symbol'}, axis = 1)
value_stocks = value_stocks.rename({'0':'symbol'}, axis = 1)
cluster_rec = cluster_rec.drop(columns= 'Unnamed: 0')

value_choices = value_stocks.set_index('symbol')
value_choices = value_choices.merge(matching, right_index = True, left_index = True)
# value_choices = value_choices.drop(columns ='Unnamed: 0')
conservative_value_stocks = value_choices[value_choices['yr_variance'] <= .45].reset_index()
moderate_value_stocks = value_choices[(value_choices['yr_variance'] <= .75) & (value_choices['yr_variance']>= .45 )].reset_index()
risky_value_stocks = value_choices[(value_choices['yr_variance'] <= 1.) & (value_choices['yr_variance'] >= .75)].reset_index()
# Top 20 Value Stocks
top_20_conservative_value = conservative_value_stocks.sort_values('avg_yr_returns', ascending = False).head(20)
top_20_moderate_value = moderate_value_stocks.sort_values('avg_yr_returns', ascending = False).head(20)
top_20_risky_value = risky_value_stocks.sort_values('avg_yr_returns', ascending = False).head(20)
# Growth Stocks
growth_choices = growth_stocks.set_index('symbol')
growth_choices = growth_choices.merge(matching, right_index = True, left_index = True)
# growth_choices = growth_choices.drop(columns ='Unnamed: 0')
conservative_growth_stocks = growth_choices[growth_choices['yr_variance'] <= .45].reset_index()
moderate_growth_stocks = growth_choices[(growth_choices['yr_variance'] <= .75) & (growth_choices['yr_variance']>= .45 )].reset_index()
risky_growth_stocks = growth_choices[(growth_choices['yr_variance'] <= 1.) & (growth_choices['yr_variance'] >= .75)].reset_index()

top_20_conservative_growth = conservative_growth_stocks.sort_values('avg_yr_returns', ascending = False).head(20)
top_20_moderate_growth = moderate_growth_stocks.sort_values('avg_yr_returns', ascending = False).head(20)
top_20_risky_growth = risky_growth_stocks.sort_values('avg_yr_returns', ascending = False).head(20)

time_horizon = time_horizon()
portfolio = user_input_choices()
recommender = processing_recommender(portfolio, cluster_rec)

app.layout = html.Div([
    dcc.Input(id='time-horizon', value='initial value', type='text'),
    html.Div(id='time-div'),
])




@app.callback(Output(component_id='time-div', component_property='children'),
            [Input(component_id='time-horizon', component_property='value')])
def time_horizon(value):
    time_investing  = value
    # while True:
    #     try:
    #         time_investing = int(time_investing)
    #         if type(time_investing) == int:
    #             break
    #     except ValueError:
    #         print('Please use digits')
    return time_investing


def user_input_choices():
    risk_tolerance = input(" ----------\n 1- Conservative\n 2- Moderate\n 3- Risky \n Please choose from the following: ").strip().lower()
    while True:
        if risk_tolerance == 'conservative' or risk_tolerance == '1':
            risk = conservative()
            break
        elif risk_tolerance == 'moderate' or risk_tolerance == '2': 
            risk = moderate()
            break
        elif risk_tolerance == 'risky' or risk_tolerance == '3':   
            risk = risky()
            break
        else:
            print("invalid input try again\n ------")
            risk_tolerance = input(" 1- Conservative\n 2- Moderate\n 3- Risky \n Please choose from the following: ").lower()
    risks = risk
    return risks



def conservative():
    counter = 0
    counter_2 = 0
    value_stocks = []
    growth_stocks = []
    portfolio = []
    Y = []
    top_picks_value = top_20_conservative_value['symbol'].tolist()
    top_picks_growth = top_20_conservative_growth['symbol'].tolist()
    full_stock_value = [top_20_conservative_growth, top_20_conservative_value]
    full_stock_value = pd.concat(full_stock_value)
    print('------------------------')
    print(top_picks_value)
    while counter < 3:
        user_input = input('Please choose 3 from the top 20 Value Stocks: ').upper()
        if user_input in top_picks_value:
            counter += 1
            value_stocks.append(user_input)
            portfolio.append(user_input)
        else:
            print('Stock Not in List')
            print('------------------------')
            print(top_picks_value)
            continue
    print('------------------------')
    print(top_picks_growth)
    while counter_2 < 7:
        user_input_2 = input('Please choose 7 from the top 20 Growth Stocks: ').upper()
        if user_input_2 in top_picks_growth:
            counter_2 += 1
            growth_stocks.append(user_input_2)
            portfolio.append(user_input_2)
        else:
            print('Stock Not in List')
            print('------------------------')
            print(top_picks_growth)
            continue
    
    for tickers in portfolio:
        df = full_stock_value[full_stock_value['symbol'] == tickers]
        Y.append(df)
    
    new_port = pd.concat(Y)
    print(new_port)
        
    return new_port

def moderate():
    counter = 0
    counter_2 = 0
    value_stocks = []
    growth_stocks = []
    portfolio = []
    top_picks_value = top_20_moderate_value['symbol'].tolist()
    top_picks_growth = top_20_moderate_growth['symbol'].tolist()
    full_stock_value = [top_20_moderate_growth, top_20_moderate_value]
    full_stock_value = pd.concat(full_stock_value)
    print('------------------------')
    print(top_picks_value)
    while counter < 5:
        user_input = input(f'Please choose 5 from the top 20 Value Stocks: ').upper()
        if user_input in top_picks_value:
            counter += 1
            value_stocks.append(user_input)
            portfolio.append(user_input)
        else:
            print('Stock Not in List')
            print('------------------------')
            print(top_picks_value)
            continue
    print('------------------------')
    print(top_picks_growth)
    while counter_2 < 5:
        user_input_2 = input('Please choose 5 from the top 20 Growth Stocks: ').upper()
        if user_input_2 in top_picks_growth:
            counter_2 += 1
            growth_stocks.append(user_input_2)
            portfolio.append(user_input_2)
        else:
            print('Stock Not in List')
            print('------------------------')
            print(top_picks_growth)
            continue
    Y = []
    for tickers in portfolio:
        df = full_stock_value[full_stock_value['symbol'] == tickers]
        Y.append(df)
    
    new_port = pd.concat(Y)
    print(portfolio)

    return new_port

def risky():
    counter = 0
    counter_2 = 0
    value_stocks = []
    growth_stocks = []
    portfolio = []
    top_picks_value = top_20_risky_value['symbol'].tolist()
    top_picks_growth = top_20_risky_growth['symbol'].tolist()
    full_stock_value = [top_20_risky_growth, top_20_risky_value]
    full_stock_value = pd.concat(full_stock_value)
    print('------------------------')
    print(top_picks_value)
    while counter < 3:
        user_input = input('Please choose 3 from the top 20 Value Stocks: ').upper()
        if user_input in top_picks_value:
            counter += 1
            value_stocks.append(user_input)
            portfolio.append(user_input)
        else:
            print('Stock Not in List')
            print('------------------------')
            print(top_picks_value)
            continue
    print('------------------------')
    print(top_picks_growth)
    while counter_2 < 8:
        user_input_2 = input('Please choose 8 from the top 20 Growth Stocks: ').upper()
        if user_input_2 in top_picks_growth:
            counter_2 += 1
            growth_stocks.append(user_input_2)
            portfolio.append(user_input_2)
        else:
            print('Stock Not in List')
            print('------------------------')
            print(top_picks_growth)
            continue
    Y = []
    for tickers in portfolio:
        df = full_stock_value[full_stock_value['symbol'] == tickers]
        Y.append(df)
    
    new_port = pd.concat(Y)
        
    return new_port   

def processing_recommender(portfolio, cluster_rec):
    cluster = portfolio
    cluster = cluster[cluster['sharpe_ratio'] >= 0]
    cluster = cluster.sort_values('sharpe_ratio', ascending = True)
    rec_test = cluster_rec.drop(columns = ['symbol','company','Price','sector'])
    rec_clust = portfolio.drop(columns = ['symbol','company','sector'])
    pip = rec_clust.sort_values('avg_yr_returns', ascending=False)
    pip = pip.index[0]
    inpt_idx = pip
    inpt = rec_test.iloc[inpt_idx]
    scores = pd.Series(index=rec_test.index)
    scores.iloc[inpt_idx] = -1
    for idx, stock in rec_test.drop(index=inpt_idx).iterrows():
        diff = 0
        for feature in stock.index:
            diff += (inpt.loc[feature]-stock.loc[feature])**2
        scores.loc[idx] = diff
    scores.sort_values()
    scores = pd.DataFrame(scores.sort_values())
    recommend_err = scores.merge(cluster_rec, left_index = True, right_index = True)
    recommend_err = recommend_err.rename({0: 'RMSE'}, axis = 1)
    testing = recommend_err.head(10)
    return testing

def monte_carlo(portfolio, time_horizon):
    sim = pd.DataFrame()
    iterations = 5000

    for x in range(iterations):
        pv = float(portfolio['Price'].sum()) + 6
        expected_return = float(portfolio['avg_yr_returns'].mean())
        volatility = float(portfolio['yr_variance'].mean())
        time_horizon = time_horizon
        annual_investment = pv
        stream = []
        for i in range(time_horizon):
            end = round(pv * (1 + np.random.normal(expected_return,volatility)) + annual_investment,2)

            stream.append(end)

            pv = end
            
        sim[x] = stream

def simulator(monte_carlo, portfolio):    
    price_per = float(portfolio['Price'].sum()) + 6
    expected_return = float(portfolio['avg_yr_returns'].mean())
    volatility = float(portfolio['yr_variance'].mean())
    print(f'price per year : {price_per}')
    print(f'expected return : {expected_return}')
    print(f'risk : {volatility}')
    print('------------------')
    amount = len(sim)-1
    ending_values = sim.loc[amount]
    p_tiles = np.percentile(ending_values,[5,10,15])
    for p in range(len(p_tiles)):
        l = [5,10,15]
        print("{}%-ile:  ".format(l[p]).rjust(15),"{}".format(locale.currency(p_tiles[p], grouping=True)))
    
    random_x = sim.index
    random_y0 = sim[1]
    random_y1 = sim[2]
    random_y2 = sim[3]
    random_y3 = sim[4]
    random_y4 = sim[5]

    # Create traces
    fig = go.Figure()
    fig.update_layout(title='Your Portfolio Outcome', 
                      xaxis_title = 'Years Invested',
                     yaxis_title = 'Return')
    fig.add_trace(go.Scatter(x=random_x, y=random_y0,
                        mode='lines+markers',
                        name='stream_1'))
    fig.add_trace(go.Scatter(x=random_x, y=random_y1,
                        mode='lines+markers',
                        name='stream_2'))
    fig.add_trace(go.Scatter(x=random_x, y=random_y2,
                        mode='lines+markers', 
                        name='stream_3'))

    fig.add_trace(go.Scatter(x=random_x, y=random_y3,
                        mode='lines+markers',
                        name='stream_4'))
    fig.add_trace(go.Scatter(x=random_x, y=random_y4,
                        mode='lines+markers', 
                        name='stream_5'))

    fig.show()




if __name__ == '__main__':
    app.run_server(port = 4050)