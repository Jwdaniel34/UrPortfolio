import pandas as pd
import pickle

# sectors_dyr = pd.DataFrame(companies.groupby(['sector','symbol','date','company'])['Dividend payout ratio'].sum())
# sectors_dyr = sectors_dyr.reset_index()
# sectors_dyr = sectors_dyr.rename({'Dividend payout ratio': 'dividend_payout_ratio'}, axis = 1)
# sectors_dyr.date = pd.to_datetime(sectors_dyr.date)
# sectors_dyr.set_index("date", inplace=True)

# symbols = sectors_dyr['symbol'].unique()
# symbols = symbols.tolist()

# stocks1 = input('Which stock would you like to see: ').upper()
# stocks2 = input('Which stock would you like to compare: ').upper()

# while True:
#     if stocks1 in symbols:
#         if stocks2 in symbols:
#             break
#         else:
#             stocks2 = input('Comparison Stock not Available please choose again: ').upper()
#     else:
#         stocks1 = input('Stock not Available please choose again: ').upper()


# symbol_1 = sectors_dyr[sectors_dyr['symbol'] == stocks1]
# symbol_2 = sectors_dyr[sectors_dyr['symbol'] == stocks2]

# company_1 = symbol_1['company'].values[0]
# company_2 = symbol_2['company'].values[0]

# trace2 = go.Scatter(x = symbol_1.index,
#                  y = symbol_1.dividend_payout_ratio,
#                  mode = 'lines+markers',
#                  name = f'{stocks1}')
# trace3 = go.Scatter(x = symbol_2.index,
#                  y = symbol_2.dividend_payout_ratio,
#                  mode = 'lines+markers',
#                  name = f'{stocks2}')
# data = [trace2,trace3]
# layout = go.Layout(title =f'{company_1} vs {company_2} Price 2000-2019 by Dividend Payout Ratio')
# figure = go.Figure(data = data, layout = layout)
# figure.show()