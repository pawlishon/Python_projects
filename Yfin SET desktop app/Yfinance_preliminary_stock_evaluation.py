# https://algotrading101.com/learn/yahoo-finance-api-guide/
from helpers.PyQTWorker import *
from model.evaluation import *
from PyQt5.QtWidgets import QMessageBox
from model import Stock_price_prediction
from view.MainWindow import *
import sys
from datetime import date
import csv
from view.RatioExplanationWindow import *
from view.DividendsWindow import *
from view.price_win_2 import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from view.reports import *
from model.financial_statements import get_financial_statements
from helpers.pandas_model import pandasModel
from helpers.file_dialog import App
import os
import importlib


class FirstApp(Ui_MainWindow):
    def __init__(self, window):
        self.setupUi(window)
        self.textBrowser.setText('Welcome')
        window.setWindowTitle('Tool for stock evaluation - by Pawel Piatkowski')
        self.AddTicker.clicked.connect(self.showInstrument)
        self.EvaluateButton.clicked.connect(self.thread)
        self.ClearButton.clicked.connect(self.ClearContent)
        self.ExportButton.clicked.connect(self.ExportContent)
        self.EvaluationProgress.setValue(0)
        self.RemoveLastButton.clicked.connect(self.Removal)
        self.ImportButton.clicked.connect(self.ImportData)
        self.WikiButton.clicked.connect(self.Wiki)
        self.DowButton.clicked.connect(self.ImportDow)
        self.SPButton.clicked.connect(self.ImportSP)
        self.DivButton.clicked.connect(self.DivHis)
        self.ForecastButton.clicked.connect(self.Prices)
        self.BrowseButton.clicked.connect(self.BrowseFiles)
        self.reportButton.clicked.connect(self.reports)
        self.instrument_list =[]
        self.Final_df = pd.DataFrame()
        self.export_number = 0
        self.threadpool = QThreadPool()
        self.futures = ()
        self.price = pd.DataFrame()


    def thread(self):
        self.EvaluateButton.setEnabled(False)
        worker = Worker(self.Evaluate)
        worker.signals.result.connect(self.show_table)
        worker.signals.progress.connect(self.progress_fn)
        self.threadpool.start(worker)

    def showInstrument(self):
        self.instrument_list.append(self.InsertField.text())
        string = ''
        for item in self.instrument_list:
            if string == '':
                string = item + ', '
            else:
                string = string + item + ', '
        self.textBrowser.setText(string)

    def Evaluate(self, progress_callback):
        #self.Final_df = ResultJoin(self.instrument_list)
        self.Final_df = pd.DataFrame()
        i = 0
        for ticker in self.instrument_list:
            temp = my_valuation(ticker)
            self.Final_df = pd.concat([self.Final_df, temp], axis=0)
            i = i + 1
            progress_callback.emit(int(i/len(self.instrument_list) * 100))
        return self.Final_df

    def progress_fn(self, n):
        self.EvaluationProgress.setValue(n)

    def show_table(self, data):
        model = pandasModel(data)
        self.tableView.setModel(model)
        self.EvaluateButton.setEnabled(True)

    def ClearContent(self):
        self.instrument_list = []
        self.textBrowser.setText('')

    def ExportContent(self):
        self.ExportToExcel(self.Final_df)

    def Removal(self):
        self.instrument_list.pop()
        string = ''
        for item in self.instrument_list:
            if string == '':
                string = item + ', '
            else:
                string = string + item + ', '
        self.textBrowser.setText(string)

    def _message(self, text, title):
        msg = QMessageBox()
        msg.setText(text)
        msg.setWindowTitle(title)
        msg.exec_()

    def ImportData(self):
        path = self.DirectoryPath.text()
        if path.endswith('.csv'):
            try:
                with open(path, newline='') as f:
                    reader = csv.reader(f)
                    data = list(reader)
                self.instrument_list = []
                for elem in data:
                    self.instrument_list.append(elem[0])
                string = ''
                for item in self.instrument_list:
                    if string == '':
                        string = item + ', '
                    else:
                        string = string + item + ', '
                self.textBrowser.setText(string)
            except:
                self._message('Invalid file format. Csv file should contain one column with header. '
                              'This column should have Yahoo finance tickers.', 'Warning')
        else:
            self._message('It is not a csv file !', 'Warning')

    def BrowseFiles(self):
        self._shared_memory = {}
        self.ex = App(self._shared_memory)
        self.DirectoryPath.setText(self._shared_memory.get('filename'))

    def Wiki(self):
        self.wiki_win = QtWidgets.QMainWindow()
        self.ui2 = Ui_SecondWindow()
        self.ui2.setupUi(self.wiki_win)
        self.wiki_win.show()
        self.ui2.WikiText.setText(
            'Trailing Annual Dividend Yield - Percentage amount of price that was distributed to shareholders as dividend in last year https://www.investopedia.com/terms/d/dividendyield.asp \n \n 5 Year Dividend Yield - average of dividend yields in last 5 years \n \n Payout Ratio - percentage amount of net income that is beign distributed to shareholders https://www.investopedia.com/terms/d/dividendpayoutratio.asp \n \n Revenue Per Share - Total revenue of company divided by share number https://www.investopedia.com/terms/s/salespershare.asp \n \n Total Debt/Equity - degree to which a company is financing its operations through debt versus wholly owned funds. 1 is considered relatively safe, while 2 is risky. https://www.investopedia.com/terms/d/debtequityratio.asp \n \n Current ratio - also known as liquidity ratio. Division of total assets to total liabilities. Its a company ability to pay short term obligations. Good current ratio is considered 1.5 - 2. https://www.investopedia.com/terms/c/currentratio.asp \n \n Book value per share - Its a ratio of equity available to common shareholders divided by number of shares. https://www.investopedia.com/terms/b/bvps.asp \n \n Recommendation - Yahoo finance analysts recommendation. 1 - 1.5 is a strong buy, 2 -3 is a buy, 3 - 4 is hold and anything less than 4 is sell or strong sell. \n \n Company Summary - short description of what company is doing \n \n PEG Ratio - its the P/E ratio divided by Earnings per share growth. Everything over 1 is expected as overvalued , while under 1 are undervalued companies. https://www.investopedia.com/terms/p/pegratio.asp \n \n Price/Sales - compares company sales price to its sales. The lower the better. https://www.investopedia.com/terms/p/price-to-salesratio.asp \n \n Price/Book - commpany stock price divided by its book value. Under 1 is considered undervalued stock. Over 1.5 indicates that high volatile is possible. https://www.investopedia.com/terms/p/price-to-bookratio.asp \n \n P/E - price to earnings ratio. One of the crucial indicator valuating company. The lower the better. Depends on the market by generally over 25 is considered overvalued. https://www.investopedia.com/terms/p/price-earningsratio.asp \n  \n Beta - indicates how big are stock price fluctuations in comparison to market volatile. 1 is same with market changes, under 1 are safer stocks and over 1 are stocks that may quickly rise or plummet. https://www.investopedia.com/investing/beta-know-risk/ \n \n 1y Target Estimate - close price estimate by yahoo finance, not very reliable in final decision. \n \n  EPS - earnings per share. The higher the more profitable the company is. https://www.investopedia.com/terms/e/eps.asp \n \n Previous close - last price of this stock in previous day.\n \n Market Cap - value of the company calculated as stock price of the company multiplied by its number of shares. Companies over 10B are considered big. https://www.investopedia.com/investing/market-capitalization-defined/ \n \n Before buying a stock its also worth checking company annual report. Pay attention if company is paying income tax (if not there might be some positions which indicate losses). Often takeovers are also not welcome, company might try to rise too quick too big. Its good when company has some cash reserves, but its not good if cash and financial activities are most of company incomes. ')
        self.wiki_win.setWindowTitle('Ratio explanation')

    def ImportDow(self):
        self.instrument_list = self.instrument_list + si.tickers_dow()
        string = ''
        for item in self.instrument_list:
            if string == '':
                string = item + ', '
            else:
                string = string + item + ', '
        self.textBrowser.setText(string)

    def ImportSP(self):
        self.instrument_list = self.instrument_list + si.tickers_sp500()
        string = ''
        for item in self.instrument_list:
            if string == '':
                string = item + ', '
            else:
                string = string + item + ', '
        self.textBrowser.setText(string)

    def DivHis(self):
        self.div_win = QtWidgets.QMainWindow()
        self.ui = Ui_DivWindow()
        self.ui.setupUi(self.div_win)
        self.ui.ShowDiv.clicked.connect(self.DHis)
        self.div_win.setWindowTitle('Dividend History')
        self.div_win.show()

    def DHis(self):
        ticker = self.ui.DivTicker.text()
        start_date = self.ui.DivDate.date().toPyDate().strftime('%d-%m-%Y')
        try:
            data = si.get_dividends(ticker, start_date)
            data = data.reset_index()
            data.columns = ['Date', 'Amount USD', 'Ticker']
            model = pandasModel(data)
            self.ui.DivView.setModel(model)
            self.ui.DivPlot.canvas.axes.clear()
            self.ui.DivPlot.canvas.axes.plot(data['Date'], data['Amount USD'])
            self.ui.DivPlot.canvas.axes.set_title('Dividends Chart')
            self.ui.DivPlot.canvas.draw()
        except:
            self._message(traceback.format_exc(), 'Information')

    def Prices(self):
        self.price_win = QtWidgets.QMainWindow()
        self.ui3 = Ui_MainWindow2()
        self.ui3.setupUi(self.price_win)
        self.price_win.setWindowTitle('Price History')
        self.price_win.show()
        self.ui3.PriceShow.clicked.connect(self.showPrices)
        self.interval = '1d'
        self.ui3.DailyInt.setChecked(True)
        self.ui3.MonthlyInt.clicked.connect(self.oneInt)
        self.ui3.DailyInt.clicked.connect(self.oneInt)
        self.ui3.WeeklyInt.clicked.connect(self.oneInt)
        self.ui3.PredictButton.clicked.connect(self.thread_arima)
        self.ui3.PredictButton_2.clicked.connect(self.PriceInInterval)
        self.ui3.progressBar.setValue(0)

    def showPrices(self):
        start_date = self.ui3.StartDate.date().toPyDate().strftime('%m/%d/%Y')
        end_date = self.ui3.EndDate.date().toPyDate().strftime('%m/%d/%Y')
        ticker = self.ui3.PriceTicker.text()
        if self.ui3.WeeklyInt.isChecked():
            self.interval = '1wk'
        elif self.ui3.MonthlyInt.isChecked():
            self.interval = '1mo'
        elif self.ui3.DailyInt.isChecked():
            self.interval = '1d'
        try:
            self.price = si.get_data(ticker, start_date=start_date, end_date=end_date, index_as_date=False, interval=self.interval)
            self.ui3.PricePlot.canvas.axes.clear()
            self.ui3.PricePlot.canvas.axes.plot(self.price['date'], self.price['close'])
            self.ui3.PricePlot.canvas.axes.set_title('Prices Chart')
            self.ui3.PricePlot.canvas.draw()
        except:
            self._message('Invalid Ticker or date.', 'Warning')
            self.ui3.PricePlot.canvas.axes.clear()

    def oneInt(self):
        if self.ui3.WeeklyInt.isChecked():
            self.ui3.DailyInt.setChecked(False)
            self.ui3.MonthlyInt.setChecked(False)
        elif self.ui3.MonthlyInt.isChecked():
            self.ui3.DailyInt.setChecked(False)
            self.ui3.WeeklyInt.setChecked(False)
        elif self.ui3.DailyInt.isChecked():
            self.ui3.WeeklyInt.setChecked(False)
            self.ui3.MonthlyInt.setChecked(False)

    def useARIMA(self, progress_callback):
        self.price['date'] = self.price.index
        self.price.reset_index(drop=True, inplace=True)
        progress_callback.emit(10)
        self.futures = Stock_price_prediction.PreditctPrices(self.price, self.interval, progress_callback)
        return self.futures

    def thread_arima(self):
        self.ui3.PredictButton.setEnabled(False)
        worker = Worker(self.useARIMA)
        worker.signals.result.connect(self.plot_predictions)
        worker.signals.error.connect(self.error_predictions)
        worker.signals.progress.connect(self.progress_predict)
        self.threadpool.start(worker)
        self.ui3.progressBar.setValue(0)

    def progress_predict(self, n):
        self.ui3.progressBar.setValue(n)

    def plot_predictions(self, predictions):
        self.ui3.PricePlot.canvas.axes.clear()
        self.ui3.PricePlot.canvas.axes.plot(self.price['date'], self.price['close'], color='blue', label='Actual Price')
        self.ui3.PricePlot.canvas.axes.plot(predictions[0], predictions[1], color='red', label='Future Price')
        self.ui3.PricePlot.canvas.axes.set_title('Prices Chart')
        self.ui3.PricePlot.canvas.axes.legend()
        self.ui3.PricePlot.canvas.draw()
        self.ui3.PredictButton.setEnabled(True)

    def error_predictions(self):
        self._message('Invalid Ticker or date. It is also possible that provided data is '
                      'not sufficient for stock price prediction.', 'Warning')
        self.ui3.PredictButton.setEnabled(True)

    def PriceInInterval(self):
        future_periods = int(self.ui3.FuturePeriods.text())
        if isinstance(future_periods,int) and len(self.futures[1])>future_periods:
            self.ui3.FuturePrice.setText(str(self.futures[1][future_periods]))
        else:
            self._message('Next interval value should be integer not greater than 10% of shown stock price history',
                          'Information')

    def ExportToExcel(self,instrument_results):
        self.export_number = self.export_number + 1
        instrument_results.to_excel('results_' + str(date.today()) + '_' + str(self.export_number) + '.xlsx', index=False)

    def reports(self):
        self.report_win = QtWidgets.QMainWindow()
        self.ui4 = Ui_MainWindow3()
        self.ui4.setupUi(self.report_win)
        self.report_win.show()
        self.report_win.setWindowTitle('Report analysis')
        self.report1 = pd.DataFrame()
        self.report2 = pd.DataFrame()
        self.ui4.reportButton_1.clicked.connect(self.report_1)
        self.ui4.reportButton_2.clicked.connect(self.report_2)
        self.ui4.comboBoxTickers.addItem('Ticker 1')
        self.ui4.comboBoxTickers.addItem('Ticker 2')
        self.ui4.comboBoxTickers.addItem('Both')
        self._possible_features =['researchDevelopment','incomeBeforeTax','netIncome','sellingGeneralAdministrative','grossProfit','operatingIncome','interestExpense','totalRevenue','costOfRevenue','grossProfitMargin','taxPaid','netRatio','totalLiab','totalStockholderEquity','totalAssets','commonStock','otherCurrentAssets','retainedEarnings','treasuryStock','cash','totalCurrentLiabilities','shortLongTermDebt','propertyPlantEquipment','totalCurrentAssets','netTangibleAssets','shortTermInvestments','netReceivables','longTermDebt','inventory','currentRatio','debtToESRatio','longOverShortDebt','depreciation','capitalExpenditures', 'returnOnShareholdersEquity']
        for i in self._possible_features:
            self.ui4.comboBoxFeatures.addItem(i)
        self.ui4.plotButton.clicked.connect(self.plot_features)

    def report_1(self):
        try:
            ticker = self.ui4.tickerInput1.text()
            self.ui4.t1_Label.setText(ticker.upper()+' (values in millions): ')
            self.report1, self.ratios1 = get_financial_statements(ticker)
            model = pandasModel(self.report1)
            model2 = pandasModel(self.ratios1)
            self.ui4.reportView1.setModel(model)
            self.ui4.reportView1_2.setModel(model2)
        except:
            self._message('Invalid ticker or no data for this identifier.', 'Information')

    def report_2(self):
        try:
            ticker = self.ui4.tickerInput2.text()
            self.ui4.t2_Label.setText(ticker.upper() + ' (values in millions): ')
            self.report2, self.ratios2 = get_financial_statements(ticker)
            model = pandasModel(self.report2)
            model2 = pandasModel(self.ratios2)
            self.ui4.reportView2.setModel(model)
            self.ui4.reportView2_2.setModel(model2)
        except:
            self._message('Invalid ticker or no data for this identifier.', 'Information')

    def plot_features(self):
        ticker_option = str(self.ui4.comboBoxTickers.currentText())
        feature_option = str(self.ui4.comboBoxFeatures.currentText())
        self.ui4.plotArea.canvas.axes.clear()
        if ticker_option == 'Ticker 1':
            if len(self.report1)!=0:
                join_table = pd.concat([self.report1, self.ratios1])
                x = join_table.columns.to_list()[1:]
                y = join_table.loc[join_table['Breakdown'] == feature_option].values.tolist()[0][1:]
                self.ui4.plotArea.canvas.axes.plot(list(reversed(x)), list(reversed(y)))
                self.ui4.plotArea.canvas.axes.set_title('Feature Chart')
                self.ui4.plotArea.canvas.draw()
            else:
                self._message('Please get the report for Ticker 1.', 'Information')
        elif ticker_option == 'Ticker 2':
            if len(self.report2) != 0:
                join_table = pd.concat([self.report2, self.ratios2])
                x = join_table.columns.to_list()[1:]
                y = join_table.loc[join_table['Breakdown'] == feature_option].values.tolist()[0][1:]
                self.ui4.plotArea.canvas.axes.plot(list(reversed(x)), list(reversed(y)))
                self.ui4.plotArea.canvas.axes.set_title('Feature Chart')
                self.ui4.plotArea.canvas.draw()
            else:
                self._message('Please get the report for Ticker 2.', 'Information')
        else:
            if len(self.report1)!=0 and len(self.report2)!=0:
                join_table1 = pd.concat([self.report1, self.ratios1])
                join_table2 = pd.concat([self.report2, self.ratios2])
                self.ui4.plotArea.canvas.axes.clear()
                x1 = join_table1.columns.to_list()[1:]
                y1 = join_table1.loc[join_table1['Breakdown'] == feature_option].values.tolist()[0][1:]
                y2 = join_table2.loc[join_table2['Breakdown'] == feature_option].values.tolist()[0][1:]
                self.ui4.plotArea.canvas.axes.plot(list(reversed(x1)), list(reversed(y1)), color='blue',
                                                    label='First Ticker')
                self.ui4.plotArea.canvas.axes.plot(list(reversed(x1)), list(reversed(y2)), color='red', label='Second Ticker')
                self.ui4.plotArea.canvas.axes.set_title('Feature Chart')
                self.ui4.plotArea.canvas.axes.legend()
                self.ui4.plotArea.canvas.draw()
            else:
                self._message('Please get the reports for both tickers.', 'Information')




def main():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = FirstApp(MainWindow)
    MainWindow.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    if '_PYIBoot_SPLASH' in os.environ and importlib.util.find_spec("pyi_splash"):
        import pyi_splash #It may show an error in your IDE but it's fine
        pyi_splash.update_text('UI Loaded ...')
        pyi_splash.close()
    main()
