from PyQt5.QtWidgets import QDialog
from view.ARIMADialog import *
from helpers.PyQTWorker import *
import yahoo_fin.stock_info as si
from model import Stock_price_prediction


class ArimaPredictions(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.bind_events()
        self.interval = '1d'
        self.threadpool = QThreadPool()

    def bind_events(self):
        self.ui.DailyInt.setChecked(True)
        self.ui.MonthlyInt.clicked.connect(self.oneInt)
        self.ui.DailyInt.clicked.connect(self.oneInt)
        self.ui.WeeklyInt.clicked.connect(self.oneInt)
        self.ui.PredictButton.clicked.connect(self.thread_arima)
        self.ui.PredictButton_2.clicked.connect(self.PriceInInterval)
        self.ui.progressBar.setValue(0)
        self.ui.PriceShow.clicked.connect(self.showPrices)

    def showPrices(self):
        start_date = self.ui.StartDate.date().toPyDate().strftime('%m/%d/%Y')
        end_date = self.ui.EndDate.date().toPyDate().strftime('%m/%d/%Y')
        ticker = self.ui.PriceTicker.text()
        if self.ui.WeeklyInt.isChecked():
            self.interval = '1wk'
        elif self.ui.MonthlyInt.isChecked():
            self.interval = '1mo'
        elif self.ui.DailyInt.isChecked():
            self.interval = '1d'
        try:
            self.price = si.get_data(ticker, start_date=start_date, end_date=end_date, index_as_date=False, interval=self.interval)
            self.ui.PricePlot.canvas.axes.clear()
            self.ui.PricePlot.canvas.axes.plot(self.price['date'], self.price['close'])
            self.ui.PricePlot.canvas.axes.set_title('Prices Chart')
            self.ui.PricePlot.canvas.draw()
        except:
            self._message('Invalid Ticker or date.', 'Warning')
            self.ui.PricePlot.canvas.axes.clear()


    def oneInt(self):
        if self.ui.WeeklyInt.isChecked():
            self.ui.DailyInt.setChecked(False)
            self.ui.MonthlyInt.setChecked(False)
        elif self.ui.MonthlyInt.isChecked():
            self.ui.DailyInt.setChecked(False)
            self.ui.WeeklyInt.setChecked(False)
        elif self.ui.DailyInt.isChecked():
            self.ui.WeeklyInt.setChecked(False)
            self.ui.MonthlyInt.setChecked(False)

    def useARIMA(self, progress_callback):
        #self.price['date'] = self.price.index
        self.price.reset_index(drop=True, inplace=True)
        progress_callback.emit(10)
        self.futures = Stock_price_prediction.PreditctPrices(self.price, self.interval, progress_callback)
        return self.futures

    def thread_arima(self):
        self.ui.PredictButton.setEnabled(False)
        worker = Worker(self.useARIMA)
        worker.signals.result.connect(self.plot_predictions)
        worker.signals.error.connect(self.error_predictions)
        worker.signals.progress.connect(self.progress_predict)
        self.threadpool.start(worker)
        self.ui.progressBar.setValue(0)

    def progress_predict(self, n):
        self.ui.progressBar.setValue(n)

    def plot_predictions(self, predictions):
        self.ui.PricePlot.canvas.axes.clear()
        self.ui.PricePlot.canvas.axes.plot(self.price['date'], self.price['close'], color='blue', label='Actual Price')
        self.ui.PricePlot.canvas.axes.plot(predictions[0], predictions[1], color='red', label='Future Price')
        self.ui.PricePlot.canvas.axes.set_title('Prices Chart')
        self.ui.PricePlot.canvas.axes.legend()
        self.ui.PricePlot.canvas.draw()
        self.ui.PredictButton.setEnabled(True)

    def error_predictions(self):
        self._message('Invalid Ticker or date. It is also possible that provided data is '
                      'not sufficient for stock price prediction.', 'Warning')
        self.ui.PredictButton.setEnabled(True)

    def PriceInInterval(self):
        future_periods = int(self.ui.FuturePeriods.text())
        if isinstance(future_periods, int) and len(self.futures[1]) > future_periods:
            self.ui.FuturePrice.setText(str(self.futures[1][future_periods]))
        else:
            self._message('Next interval value should be integer not greater than 10% of shown stock price history',
                          'Information')

    def _message(self, text, title):
        msg = QMessageBox()
        msg.setText(text)
        msg.setWindowTitle(title)
        msg.exec_()

