import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style

style.use('fivethirtyeight')

bridge_height = {'meters': [10.26, 10.31, 10.27, 10.22, 10.23, 6212.42, 10.28, 10.25, 10.31]}
df = pd.DataFrame(bridge_height)
df['STD'] = pd.rolling_std(df['meters'], 2)

df_std = df.describe()['meters']['std']  # find the standard deviation of the meters column
df_clean = df[df['STD'] < df_std]  # clean data so only points below std are shown


df_clean['meters'].plot()
plt.show()


