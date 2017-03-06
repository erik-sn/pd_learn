import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from matplotlib import style

style.use('ggplot')

web_stats = {
    'Day': [1, 2, 3, 4, 5, 6],
    'Visitors': [43, 53, 34, 45, 64, 34],
    'Bounce_Rate': [65, 72, 62, 64, 54, 66],
}

df = pd.DataFrame(web_stats)


# seleting top or bottom of data frame
# print(df.head(2))
# print(df.tail())


# setting column as index - immutable, returns new data frame
# print(df.set_index('Day'))
# df = df.set_index('Day')
# # or
# df.set_index('Day', inplace=True)


# # reference a column
# print(df['Visitors'])
# print(df.Visitors)  # use underscores in variables to allow for this (Bounce_rate vs Bounce Rate)


# # reference multiple columns
# print(df[['Bounce_Rate', 'Visitors']])


# converting back to python list
print(df.Visitors.tolist())
# print(df[['Bounce_Rate', 'Visitors']].tolist())  # error
np_array = np.array(df[['Bounce_Rate', 'Visitors']])  # use numpy
print(np_array)

# and back to dataframe
print(pd.DataFrame(np_array))

