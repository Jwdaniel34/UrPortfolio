import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from functions import *
import locale
locale.setlocale(locale.LC_ALL, 'en_CA.UTF-8')

def conservative():
    value_stocks = []
    growth_stocks = []
    portfolio = []
    top_picks_value = top_20_conservative_value['symbol'].tolist()
    top_picks_growth = top_20_conservative_growth['symbol'].tolist()
    full_stock_value = [top_20_conservative_growth, top_20_conservative_value]
    full_stock_value = pd.concat(full_stock_value)
    Y = pd.DataFrame(columns = full_stock_value.columns)
    user_input = st.multiselect(label = 'Please choose 7 from the top 20 Value Stocks:', options =top_picks_value)
    value_stocks.extend(user_input)
    portfolio.extend(user_input)
    user_input_2 = st.multiselect(label = 'Please choose 3 from the top 20 Growth Stocks: ', options= top_picks_growth)
    growth_stocks.extend(user_input_2)
    portfolio.extend(user_input_2)
    # st.write(portfolio)
    for tickers in portfolio:
        df = full_stock_value[full_stock_value['symbol'] == tickers]
        Y = pd.concat([Y, df])

    return Y


def moderate():
    value_stocks = []
    growth_stocks = []
    portfolio = []
    top_picks_value = top_20_moderate_value['symbol'].tolist()
    top_picks_growth = top_20_moderate_growth['symbol'].tolist()
    full_stock_value = [top_20_moderate_growth, top_20_moderate_value]
    full_stock_value = pd.concat(full_stock_value)
    Y = pd.DataFrame(columns = full_stock_value.columns)
    user_input = st.multiselect(label = 'Please choose 5 from the top 20 Value Stocks:', options =top_picks_value)
    value_stocks.extend(user_input)
    portfolio.extend(user_input)
    user_input_2 = st.multiselect(label = 'Please choose 5 from the top 20 Growth Stocks: ', options= top_picks_growth)
    growth_stocks.extend(user_input_2)
    portfolio.extend(user_input_2)
    # st.write(portfolio)
    for tickers in portfolio:
        df = full_stock_value[full_stock_value['symbol'] == tickers]
        Y = pd.concat([Y, df])
    return Y

def risky():
    value_stocks = []
    growth_stocks = []
    portfolio = []
    top_picks_value = top_20_risky_value['symbol'].tolist()
    top_picks_growth = top_20_risky_growth['symbol'].tolist()
    full_stock_value = [top_20_risky_growth, top_20_risky_value]
    full_stock_value = pd.concat(full_stock_value)
    Y = pd.DataFrame(columns = full_stock_value.columns)
    user_input = st.multiselect(label = 'Please choose 3 from the top 20 Value Stocks:', options =top_picks_value)
    value_stocks.extend(user_input)
    portfolio.extend(user_input)
    user_input_2 = st.multiselect(label = 'Please choose 8 from the top 20 Growth Stocks: ', options= top_picks_growth)
    growth_stocks.extend(user_input_2)
    portfolio.extend(user_input_2)
    # st.write(portfolio)
    for tickers in portfolio:
        df = full_stock_value[full_stock_value['symbol'] == tickers]
        Y = pd.concat([Y, df])
    return Y


def simulator(portfolio, time_horizon):
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
    price_per = round(float(portfolio['Price'].sum()),2) + 6
    expected_return = round(float(portfolio['avg_yr_returns'].mean()),3)
    volatility = round(float(portfolio['yr_variance'].mean()),3)
    st.write('price to invest per year : ', price_per)
    st.write('expected return :', expected_return)
    st.write('expected risk :', volatility)
    amount = len(sim)-1
    ending_values = sim.loc[amount]
    p_tiles = np.percentile(ending_values,[5,10,15])
    for p in range(len(p_tiles)):
        l = [5,10,15]
        st.subheader('Possible Return Each Year')
        st.write("{}%-percentile:  ".format(l[p]).rjust(15),"{}".format(locale.currency(p_tiles[p], grouping=True)))
    
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

    return fig


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
    recommend_err = recommend_err.drop(columns = 'RMSE', axis = 1)
    testing = recommend_err.head(10)
    return testing


image = Image.open('stocks_icons.png')
st.image(image, caption='', use_column_width=False)

st.title('Investors Portfolio - Welcome to StockUp')


st.subheader('How long would you like to invest for?')
time_horizon = st.slider(label= '', min_value = 0, max_value = 30, value = 2,step = 1)
st.write('Years Investing:', time_horizon)

st.subheader("What's your risk tolerance")
risk_tolerance = st.radio( "Risk tolerance level",  
                ('Conservative', 'Moderate', 'Risky'))
if risk_tolerance == 'Conservative':
    risk = conservative()
    st.write(simulator(risk,time_horizon))
elif risk_tolerance == 'Moderate': 
    risk = moderate()
    st.write(simulator(risk,time_horizon))
elif risk_tolerance == 'Risky':   
    risk = risky()
    st.write(simulator(risk,time_horizon))
else:
   st.write("You didn't select a risk tolerance.")


st.subheader("Recommended Stocks Based on Selection")
st.write(processing_recommender(risk,cluster_rec))
rec_portfolio = processing_recommender(risk, cluster_rec)