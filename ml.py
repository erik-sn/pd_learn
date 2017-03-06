import pandas as pd
import numpy as np
from matplotlib import style
from statistics import mean
from sklearn import svm, preprocessing, model_selection

style.use('fivethirtyeight')


def create_labels(cur_hpi, fut_hpi):
    return 1 if fut_hpi > cur_hpi else 0


def moving_average(values):
    return mean(values)

housing_data = pd.read_pickle('files/hpi_final.pickle')

# clean data
housing_data = housing_data.pct_change()
housing_data.replace([np.inf, -np.inf], np.nan, inplace=True)  # convert infinity values to nan
housing_data = housing_data.dropna()  # first value can't do a percent change (nothing to compare to!)

housing_data['US_HPI_FUTURE'] = housing_data['USA'].shift(-1)  # shift values forward so we can see if past values predict
# print(housing_data[['USA', 'US_HPI_FUTURE']].head())

# mapping function over a data set
housing_data['label'] = list(map(create_labels, housing_data['USA'], housing_data['US_HPI_FUTURE']))
# print(housing_data.head())
# housing_data['ma_apply_example'] = pd.rolling_apply(housing_data['M30'], 10, moving_average)
# print(housing_data.tail())

X = np.array(housing_data.drop(['label', 'US_HPI_FUTURE'], 1).dropna())
X = preprocessing.scale(X)
y = np.array(housing_data['label'])

X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.2)

clf = svm.SVC(kernel='linear')
clf.fit(X_train, y_train)

print(X_train)

print(clf.score(X_test, y_test))
