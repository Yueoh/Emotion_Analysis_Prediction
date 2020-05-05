# fit an ARIMA model
from pandas import read_csv
from matplotlib import pyplot
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from math import sqrt
# load dataset
series = read_csv('t_emotion.csv', header=0, index_col=0)
data=series['disgust']

train, test = data[:1441], data[1441:]

dataset = train
# walk forward over time steps in test
values = dataset.values
history = [values[i] for i in range(len(values))]
predictions = list()
test_values = test.values
print(len(test_values))
for t in range(len(test_values)):
    # fit model
    model = ARIMA(history, order=(10,0,0))
    model_fit = model.fit(trend='nc', disp=0)
    # make prediction
    yhat = model_fit.forecast()[0]
    predictions.append(yhat)
    history.append(test_values[t])
    print(len(predictions))
    print(predictions)
rmse = sqrt(mean_squared_error(test_values, predictions))
print('RMSE: %.3f' %  rmse)
mae = mean_absolute_error(test_values, predictions)
print('MAE: %.3f' %  mae)
