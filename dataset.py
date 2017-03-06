import quandl
import pandas as pd
import pickle
import matplotlib.pyplot as plt
from matplotlib import style

from constants import QUANDL_API

style.use('fivethirtyeight')




def state_list():
    return pd.read_html('https://simple.wikipedia.org/wiki/List_of_U.S._states')[0]


def percent_change(df, key):
    df[key] = (df[key] - df[key][0]) / df[key][0] * 100  # percent change from start
    return df


def get_initial_state_data():
    abbreviations = state_list()[0]
    main_df = pd.DataFrame()
    for abbr in abbreviations[1:]:
        df = quandl.get('FMAC/HPI_{}'.format(abbr), authtoken=QUANDL_API)
        df.rename(columns={'Value': abbr}, inplace=True)  # column name should be unique
        df = percent_change(df, abbr)

        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df)

    main_df.to_pickle('files/state_abbr_hpi_pandas.pickle')


def hpi_benchmark():
    df = quandl.get('FMAC/HPI_USA', authtoken=QUANDL_API)
    df.rename(columns={'Value': 'USA'}, inplace=True)  # column name should be unique
    df = percent_change(df, 'USA')
    return df


def mortgage_30y():
    df = quandl.get('FMAC/MORTG', trim_start='1975-01-01', authtoken=QUANDL_API)
    df = percent_change(df, 'Value')
    df = df.resample('M', how='sum')
    df.columns = ['M30']
    return df


def sp500_data():
    df = quandl.get("YAHOO/INDEX_GSPC", trim_start="1975-01-01", authtoken=QUANDL_API)
    df = percent_change(df, 'Adjusted Close')
    df = df.resample('M').mean()
    df.rename(columns={'Adjusted Close': 'sp500'}, inplace=True)
    df = df['sp500']
    return df


def gdp_data():
    df = quandl.get("BCB/4385", trim_start="1975-01-01", authtoken=QUANDL_API)
    df = percent_change(df, 'Value')
    df = df.resample('M').mean()
    df.rename(columns={'Value': 'GDP'}, inplace=True)
    df = df['GDP']
    return df


def us_unemployment():
    df = quandl.get("ECPI/JOB_G", trim_start="1975-01-01", authtoken=QUANDL_API)
    df = percent_change(df, 'Unemployment Rate')
    df = df.resample('1D').mean()
    df = df.resample('M').mean()
    return df

# # reading pickles
# with open('files/state_abbr_hpi.pickle', 'rb') as pickle_in:
#     hpi_data = pickle.load(pickle_in)
#     print(hpi_data)
#
#
#     # pickling with pandas
#     hpi_data.to_pickle('files/state_abbr_hpi_pandas.pickle')
#     hpi_data_pd = pd.read_pickle('files/state_abbr_hpi_pandas.pickle')
#     print(hpi_data)


# get_initial_state_data()
sp500 = sp500_data()
gpd_us = gdp_data()
unemployment = us_unemployment()
m30 = mortgage_30y()
hpi_data = pd.read_pickle('files/state_abbr_hpi_pandas.pickle')
hpi_usa = hpi_benchmark()


# plotting
# fig = plt.figure()
# ax1 = plt.subplot2grid((2, 1), (0, 0))
# ax2 = plt.subplot2grid((2, 1), (1, 0), sharex=ax1)

#
# hpi_data.plot(ax=ax1, linewidth=1)
# hpi_usa.plot(ax=ax1, color='k', linewidth=3)
#

"""
Analysis
"""

# # correlations
# hpi_state_correlation = hpi_data.corr()
#
# # description of correlation
# description = hpi_state_correlation.describe()



"""
Resampling
"""
# http://pandas.pydata.org/pandas-docs/stable/timeseries.html#offset-aliases
# mean is default
# hpi_data['TX1YR'] = hpi_data['TX'].resample('A', how='mean')
# tx_hlc = hpi_data['TX'].resample('A', how='ohlc')
#
# print(hpi_data[['TX', 'TX1YR']])
#
# hpi_data['TX'].plot(ax=ax1, label='Monthly TX HPI')
# tx_1yr.plot(ax=ax1, label='Yearly TX HPI')
# tx_hlc.plot(ax=ax1, label='HLC', linewidth=1)

"""
Handling NaN
"""
# hpi_data['TX1YR'] = hpi_data['TX'].resample('A', how='mean')  # create dataframe with NaN
#
# how_many_nulls = hpi_data.isnull().values.sum()  # count how many NaNs in data set
# print(how_many_nulls)
#
# hpi_nan1 = hpi_data.dropna()  # remove all rows that have NaN
# hpi_nan2 = hpi_data.dropna(how='all')  # remove all rows where all columns are NaN
# # forward fill - previous values and fill in forward
# # limit is the maximum consecutive values to fill
# hpi_nan3 = hpi_data.fillna(method='ffill', limit=10)
# hpi_nan4 = hpi_data.fillna(method='bfill')  # backwards fill
# hpi_nan5 = hpi_data.fillna(0)  # specify a value

"""
Rolling

rolling mean = moving average
"""
# hpi_data['TX12MA'] = pd.rolling_mean(hpi_data['TX'], 12)
# hpi_data['TX12STD'] = pd.rolling_std(hpi_data['TX'], 12)
# # hpi_data.dropna(inplace=True)  # can't roll first 11 points, can dropna for them
#
# hpi_data[['TX', 'TX12MA']].plot(ax=ax1)
# hpi_data[['TX12STD']].plot(ax=ax2)


# # rolling correlation
# sc_ga_corr = pd.rolling_corr(hpi_data['SC'], hpi_data['GA'], 12)
# hpi_data['GA'].plot(ax=ax1, label='GA')
# hpi_data['SC'].plot(ax=ax1, label='SC')
#
# ax1.legend(loc=4)
# sc_ga_corr.plot(ax=ax2, label='Correlation')
#
# plt.legend(loc=4)
# plt.show()

"""
adding Additional metrics
"""
hpi = hpi_data.join([m30, unemployment, gpd_us, sp500, hpi_usa])
hpi.dropna(inplace=True)
hpi.to_pickle('files/hpi_final.pickle')
