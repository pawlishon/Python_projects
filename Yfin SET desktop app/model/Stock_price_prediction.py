from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
from datetime import timedelta
import warnings
from dateutil.relativedelta import *

warnings.filterwarnings("ignore")

def PreditctPrices(df, interval, progress_callback):
    train_data, test_data = df[0:int(len(df)*0.8)], df[int(len(df)*0.8):]
    training_data = train_data['close'].values
    test_data = test_data['close'].values

    # Stationarity of the model
    prices = df.close
    d = 0
    result = adfuller(prices.dropna())
    while result[1] > 0.05:
        prices = prices.diff()
        result = adfuller(prices.dropna())
        d = d + 1

    progress_callback.emit(10)
    # Grid Search
    N_test_observations = len(test_data)
    lowest_MSE_err = 99999999
    i = 0
    for p in range(1, 6):
        for q in range(1,6):
            history = [x for x in training_data]
            model_predictions = []
            i = i + 1
            progress_callback.emit(10 + round(int(i / 36 * 100)))
            try:
                for time_point in range(N_test_observations):
                    model = ARIMA(history, order=(p, d, q))
                    model_fit = model.fit(disp=0)
                    output = model_fit.forecast()
                    yhat = output[0]
                    model_predictions.append(yhat)
                    true_test_value = test_data[time_point]
                    history.append(true_test_value)
                MSE_error = mean_squared_error(test_data, model_predictions)
                if MSE_error<lowest_MSE_err:
                    lowest_MSE_err = MSE_error
                    params = [p, d, q]
            except:
                None


    # Best model predictions
    history = [x for x in training_data]
    model_predictions = []

    for time_point in range(N_test_observations):
        model = ARIMA(history, order=(params[0], params[1], params[2]))
        model_fit = model.fit(disp=0)
        output = model_fit.forecast()
        yhat = output[0]
        model_predictions.append(yhat)
        true_test_value = test_data[time_point]
        history.append(true_test_value)

    # How the model did
    # test_set_range = df[int(len(df)*0.8):].date
    # plt.plot(test_set_range, model_predictions, color='blue', marker='o', linestyle='dashed',label='Predicted Price')
    # plt.plot(test_set_range, test_data, color='red', label='Actual Price')
    # plt.title('Amazon Prices Prediction')
    # plt.xlabel('Date')
    # plt.ylabel('Prices')
    # plt.legend()
    # plt.show()

    # Future predictions
    predicted_period = round(0.3 * len(df))
    full_history = [x for x in df['close'].values]
    future_predictions = []
    # N_test_observations = len(test_data)

    for time_point in range(predicted_period):
        model = ARIMA(full_history, order=(params[0], params[1], params[2]))
        model_fit = model.fit(disp=0)
        output = model_fit.forecast()
        yhat = output[0]
        future_predictions.append(yhat)
        full_history.append(yhat)

    # Future dates
    future_dates = []
    for next_period in range(len(future_predictions)):
        if interval == '1wk':
            future_dates.append(df.date.iloc[-1]+timedelta(weeks=+next_period))
        elif interval == '1d':
            future_dates.append(df.date.iloc[-1] + timedelta(days=+next_period))
        else:
            future_dates.append(df.date.iloc[-1] + relativedelta(months=+next_period))
    future_dates.insert(0, df.date.iloc[-1])
    future_predictions.insert(0, df.close.iloc[-1])
    progress_callback.emit(100)

    return future_dates, future_predictions



