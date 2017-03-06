import pandas as pd
from os.path import join

from constants import ROOT_DIR

csv_file = join(ROOT_DIR, 'charleston.csv')
output_file = join(ROOT_DIR, 'new_charleston.csv')
json_file = join(ROOT_DIR, 'new_charleston.json')

# read csv file, set date as index index
# changing a column to the index removes it as a column
df = pd.read_csv(csv_file)
df = df.set_index('Date')

# in one line
df2 = pd.read_csv(csv_file, index_col=0)

# rename file
df.columns = ['Charleston_HPI']
print(df.head())

# output csv file
df.to_csv(output_file)
df.to_csv(output_file, header=False)  # without header

# set column names and index on read
df = pd.read_csv(output_file, names=['Date', 'Charleston_HPI'], index_col=0)

# rename columns
df.rename(columns={'Charleston_HPI': 'CH'}, inplace=True)
print(df)