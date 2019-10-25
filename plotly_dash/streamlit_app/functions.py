import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics import mean_squared_error
from math import sqrt
import matplotlib.pyplot as plt
from matplotlib import style
from scipy.stats import norm
import plotly.graph_objects as go
import numpy as np
import streamlit as st
import inquirer
import pickle
# allows currency formatting
import locale
locale.setlocale(locale.LC_ALL, 'en_CA.UTF-8')
style.use('ggplot')

cluster_rec = pd.read_csv('/Users/flatironschool/UrPortfolio/recommendation_system/rec_csvs/clusters_rec.csv')
growth_stocks = pd.read_csv('/Users/flatironschool/UrPortfolio/recommendation_system/rec_csvs/growth_stocks.csv')
value_stocks = pd.read_csv('/Users/flatironschool/UrPortfolio/recommendation_system/rec_csvs/value_stocks.csv')
predictions = pd.read_csv('/Users/flatironschool/UrPortfolio/recommendation_system/rec_csvs/prediction_gv.csv')
growth_stocks = growth_stocks.rename({'0':'symbol'}, axis = 1)
value_stocks = value_stocks.rename({'0':'symbol'}, axis = 1)
cluster_rec = cluster_rec.drop(columns= 'Unnamed: 0')
matching = cluster_rec.set_index('symbol')
value_choices = value_stocks.set_index('symbol')
value_choices = value_choices.merge(matching, right_index = True, left_index = True)
# value_choices = value_choices.drop(columns ='Unnamed: 0')
conservative_value_stocks = value_choices[value_choices['yr_variance'] <= .45].reset_index()
moderate_value_stocks = value_choices[(value_choices['yr_variance'] <= .55) & (value_choices['yr_variance']>= .45 )].reset_index()
risky_value_stocks = value_choices[(value_choices['yr_variance'] <= 1.) & (value_choices['yr_variance'] >= .55)].reset_index()
# Top 20 Value Stocks
top_20_conservative_value = conservative_value_stocks.sort_values('avg_yr_returns', ascending = False).head(20)
top_20_moderate_value = moderate_value_stocks.sort_values('avg_yr_returns', ascending = False).head(20)
top_20_risky_value = risky_value_stocks.sort_values('avg_yr_returns', ascending = False).head(20)
# Growth Stocks
growth_choices = growth_stocks.set_index('symbol')
growth_choices = growth_choices.merge(matching, right_index = True, left_index = True)
# growth_choices = growth_choices.drop(columns ='Unnamed: 0')
conservative_growth_stocks = growth_choices[growth_choices['yr_variance'] <= .45].reset_index()
moderate_growth_stocks = growth_choices[(growth_choices['yr_variance'] <= .55) & (growth_choices['yr_variance']>= .45 )].reset_index()
risky_growth_stocks = growth_choices[(growth_choices['yr_variance'] <= 1.) & (growth_choices['yr_variance'] >= .55)].reset_index()

top_20_conservative_growth = conservative_growth_stocks.sort_values('avg_yr_returns', ascending = False).head(20)
top_20_moderate_growth = moderate_growth_stocks.sort_values('avg_yr_returns', ascending = False).head(20)
top_20_risky_growth = risky_growth_stocks.sort_values('avg_yr_returns', ascending = False).head(20)

