

# https://algotrading101.com/learn/yahoo-finance-api-guide/
import yfinance as yf
import yahoo_fin.stock_info as si
import pandas as pd
import requests
from PyQt5.QtWidgets import QMessageBox
import Stock_price_prediction
from MainWindow import *
import sys
from PyQt5.QtCore import QAbstractTableModel, Qt
from datetime import date
import csv
from RatioExplanationWindow import *
from DividendsWindow import *
from PricesWindow import *



def my_valuation(ticker):
    # Quote table
    try:
        key_attributes_quote = ['PE Ratio (TTM)', 'Beta (5Y Monthly)', '1y Target Est', 'EPS (TTM)',
                                'Previous Close', 'Market Cap']
        quote = si.get_quote_table(ticker)
        attr_results = []
        for attribute in key_attributes_quote:
            attr_results.append(quote[attribute])
        attr_results_df = pd.DataFrame([attr_results], columns=key_attributes_quote)
        attr_results_df['Ticker'] = ticker

    # Stats table
        stats_table = si.get_stats(ticker)
        stats_table = stats_table.iloc[[22, 23, 24, 36, 46, 47, 48], :].transpose()
        stats_table.columns = stats_table.iloc[0, :]
        stats_table = stats_table.iloc[1, :]
        stats_table = pd.DataFrame(stats_table)
        stats_table = stats_table.transpose().reset_index(drop=True)

    # Stats valuation
        val = si.get_stats_valuation(ticker).iloc[[4, 5, 6], :].transpose()
        val.columns = val.iloc[0, :]
        val = val.iloc[1, :]
        val = pd.DataFrame(val)
        val = val.transpose().reset_index(drop=True)
    # Analysts recommendation
        lhs_url = 'https://query2.finance.yahoo.com/v10/finance/quoteSummary/'
        rhs_url = '?formatted=true&crumb=swg7qs5y9UP&lang=en-US&region=US&'               \
                  'modules=upgradeDowngradeHistory,recommendationTrend,'               \
                  'financialData,earningsHistory,earningsTrend,industryTrend&'               \
                  'corsDomain=finance.yahoo.com'
              
        url = lhs_url + ticker + rhs_url
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                                 'like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        r = requests.get(url, headers=headers)
        if not r.ok:
            recommendation = 6
        try:
            result = r.json()['quoteSummary']['result'][0]
            recommendation = result['financialData']['recommendationMean']['fmt']
        except:
            recommendation = 6
        stats_table['Recommendation'] = recommendation

    # Adding business summary
        comp_ticker = yf.Ticker(ticker)
        stats_table['Company Summary'] = comp_ticker.info['longBusinessSummary']

    # join
        horizontal_stack = pd.concat([stats_table, val, attr_results_df], axis=1)

    # Changing columns order
        cols = horizontal_stack.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        horizontal_stack = horizontal_stack[cols]
        return horizontal_stack
    except:
        a = pd.DataFrame(columns=['Ticker', 'Trailing Annual Dividend Yield 3', '5 Year Average Dividend Yield 4',
                                  'Payout Ratio 4', 'Revenue Per Share (ttm)', 'Total Debt/Equity (mrq)',
                                  'Current Ratio (mrq)',
                                  'Book Value Per Share (mrq)', 'Recommendation', 'Company Summary',
                                  'PEG Ratio (5 yr expected) 1', 'Price/Sales (ttm)', 'Price/Book (mrq)',
                                  'PE Ratio (TTM)',
                                  'Beta (5Y Monthly)', '1y Target Est', 'EPS (TTM)', 'Previous Close', 'Market Cap'])
        a.loc[0] = [ticker, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
        return a


def ResultJoin(my_list):
    instrument_results = pd.DataFrame()
    for ticker in my_list:
        temp = my_valuation(ticker)
        instrument_results = pd.concat([instrument_results, temp], axis=0)
    return instrument_results


def ExportToExcel(instrument_results):
    global export_num
    export_num = export_num + 1
    instrument_results.to_excel('results_' + str(date.today()) + '_' + str(export_num) + '.xlsx', index=False)

class App(QtWidgets.QWidget):

    def __init__(self, shared):
        super().__init__()
        self.title = 'PyQt5 file dialogs - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.shared = shared
        self.initUI()


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.openFileNameDialog()


    def openFileNameDialog(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Choose File", "", "All Files (*);;Csv Files (*.csv)",
                                                            options=options)
        if fileName:
            self.shared['filename'] = fileName
            return fileName

class pandasModel(QAbstractTableModel):

    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent =None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
            return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None


class FirstApp(Ui_MainWindow):
    def __init__(self, window):
        self.setupUi(window)
        self.textBrowser.setText('Welcome')
        window.setWindowTitle('Tool for stock evaluation - by Pawel Piatkowski')
        self.AddTicker.clicked.connect(self.showInstrument)
        self.EvaluateButton.clicked.connect(self.Evaluate)
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

    def showInstrument(self):
        global instrument_list
        instrument_list.append(self.InsertField.text())
        string = ''
        for item in instrument_list:
            if string == '':
                string = item + ', '
            else:
                string = string + item + ', '
        self.textBrowser.setText(string)

    def Evaluate(self):
        global Final_df
        # Final_df = ResultJoin(instrument_list)
        Final_df = pd.DataFrame()
        i = 0
        for ticker in instrument_list:
            temp = my_valuation(ticker)
            Final_df = pd.concat([Final_df, temp], axis=0)
            i = i + 1
            progress = int(i/len(instrument_list) * 100)
            self.EvaluationProgress.setValue(progress)
        model = pandasModel(Final_df)
        self.tableView.setModel(model)

    def ClearContent(self):
        global instrument_list
        instrument_list = []
        self.textBrowser.setText('')

    def ExportContent(self):
        ExportToExcel(Final_df)

    def Removal(self):
        global instrument_list
        instrument_list.pop()
        string = ''
        for item in instrument_list:
            if string == '':
                string = item + ', '
            else:
                string = string + item + ', '
        self.textBrowser.setText(string)

    def _message(self,text, title):
        msg = QMessageBox()
        msg.setText(text)
        msg.setWindowTitle(title)
        msg.exec_()

    def ImportData(self):
        global instrument_list
        path = self.DirectoryPath.text()
        if path.endswith('.csv'):
            try:
                with open(path, newline='') as f:
                    reader = csv.reader(f)
                    data = list(reader)
                instrument_list = []
                for elem in data:
                    instrument_list.append(elem[0])
                string = ''
                for item in instrument_list:
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
        global wiki_win
        self.wiki_win = QtWidgets.QMainWindow()
        self.ui2 = Ui_SecondWindow()
        self.ui2.setupUi(self.wiki_win)
        self.wiki_win.show()
        self.ui2.WikiText.setText(
            'Trailing Annual Dividend Yield - Percentage amount of price that was distributed to shareholders as dividend in last year https://www.investopedia.com/terms/d/dividendyield.asp \n \n 5 Year Dividend Yield - average of dividend yields in last 5 years \n \n Payout Ratio - percentage amount of net income that is beign distributed to shareholders https://www.investopedia.com/terms/d/dividendpayoutratio.asp \n \n Revenue Per Share - Total revenue of company divided by share number https://www.investopedia.com/terms/s/salespershare.asp \n \n Total Debt/Equity - degree to which a company is financing its operations through debt versus wholly owned funds. 1 is considered relatively safe, while 2 is risky. https://www.investopedia.com/terms/d/debtequityratio.asp \n \n Current ratio - also known as liquidity ratio. Division of total assets to total liabilities. Its a company ability to pay short term obligations. Good current ratio is considered 1.5 - 2. https://www.investopedia.com/terms/c/currentratio.asp \n \n Book value per share - Its a ratio of equity available to common shareholders divided by number of shares. https://www.investopedia.com/terms/b/bvps.asp \n \n Recommendation - Yahoo finance analysts recommendation. 1 - 1.5 is a strong buy, 2 -3 is a buy, 3 - 4 is hold and anything less than 4 is sell or strong sell. \n \n Company Summary - short description of what company is doing \n \n PEG Ratio - its the P/E ratio divided by Earnings per share growth. Everything over 1 is expected as overvalued , while under 1 are undervalued companies. https://www.investopedia.com/terms/p/pegratio.asp \n \n Price/Sales - compares company sales price to its sales. The lower the better. https://www.investopedia.com/terms/p/price-to-salesratio.asp \n \n Price/Book - commpany stock price divided by its book value. Under 1 is considered undervalued stock. Over 1.5 indicates that high volatile is possible. https://www.investopedia.com/terms/p/price-to-bookratio.asp \n \n P/E - price to earnings ratio. One of the crucial indicator valuating company. The lower the better. Depends on the market by generally over 25 is considered overvalued. https://www.investopedia.com/terms/p/price-earningsratio.asp \n  \n Beta - indicates how big are stock price fluctuations in comparison to market volatile. 1 is same with market changes, under 1 are safer stocks and over 1 are stocks that may quickly rise or plummet. https://www.investopedia.com/investing/beta-know-risk/ \n \n 1y Target Estimate - close price estimate by yahoo finance, not very reliable in final decision. \n \n  EPS - earnings per share. The higher the more profitable the company is. https://www.investopedia.com/terms/e/eps.asp \n \n Previous close - last price of this stock in previous day.\n \n Market Cap - value of the company calculated as stock price of the company multiplied by its number of shares. Companies over 10B are considered big. https://www.investopedia.com/investing/market-capitalization-defined/ \n \n Before buying a stock its also worth checking company annual report. Pay attention if company is paying income tax (if not there might be some positions which indicate losses). Often takeovers are also not welcome, company might try to rise too quick too big. Its good when company has some cash reserves, but its not good if cash and financial activities are most of company incomes. ')
        self.wiki_win.setWindowTitle('Ratio explanation')

    def ImportDow(self):
        global instrument_list
        instrument_list = instrument_list + si.tickers_dow()
        string = ''
        for item in instrument_list:
            if string == '':
                string = item + ', '
            else:
                string = string + item + ', '
        self.textBrowser.setText(string)

    def ImportSP(self):
        global instrument_list
        instrument_list = instrument_list + si.tickers_sp500()
        string = ''
        for item in instrument_list:
            if string == '':
                string = item + ', '
            else:
                string = string + item + ', '
        self.textBrowser.setText(string)

    def DivHis(self):
        global div_win
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
            self._message('No dividend history or invalid identifier', 'Information')

    def Prices(self):
        global price_win, interval
        self.price_win = QtWidgets.QMainWindow()
        self.ui3 = Ui_Form()
        self.ui3.setupUi(self.price_win)
        self.price_win.setWindowTitle('Price History')
        self.price_win.show()
        self.ui3.PriceShow.clicked.connect(self.showPrices)
        interval = '1d'
        self.ui3.DailyInt.setChecked(True)
        self.ui3.MonthlyInt.clicked.connect(self.oneInt)
        self.ui3.DailyInt.clicked.connect(self.oneInt)
        self.ui3.WeeklyInt.clicked.connect(self.oneInt)
        self.ui3.PredictButton.clicked.connect(self.useARIMA)
        self.ui3.PredictButton_2.clicked.connect(self.PriceInInterval)

    def showPrices(self):
        global interval
        start_date = self.ui3.StartDate.date().toPyDate().strftime('%m/%d/%Y')
        end_date = self.ui3.EndDate.date().toPyDate().strftime('%m/%d/%Y')
        ticker = self.ui3.PriceTicker.text()
        if self.ui3.WeeklyInt.isChecked():
            interval = '1wk'
        elif self.ui3.MonthlyInt.isChecked():
            interval = '1mo'
        elif self.ui3.DailyInt.isChecked():
            interval = '1d'
        try:
            price = si.get_data(ticker, start_date=start_date, end_date=end_date, index_as_date=False, interval=interval)
            self.ui3.PricePlot.canvas.axes.clear()
            self.ui3.PricePlot.canvas.axes.plot(price['date'], price['close'])
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

    def useARIMA(self):
        global interval,futures
        start_date = self.ui3.StartDate.date().toPyDate().strftime('%m/%d/%Y')
        end_date = self.ui3.EndDate.date().toPyDate().strftime('%m/%d/%Y')
        ticker = self.ui3.PriceTicker.text()
        if self.ui3.WeeklyInt.isChecked():
            interval = '1wk'
        elif self.ui3.MonthlyInt.isChecked():
            interval = '1mo'
        elif self.ui3.DailyInt.isChecked():
            interval = '1d'
        try:
            price = si.get_data(ticker, start_date=start_date, end_date=end_date, interval=interval)
            price['date'] = price.index
            price.reset_index(drop=True, inplace=True)
            futures = Stock_price_prediction.PreditctPrices(price,interval)
            self.ui3.PricePlot.canvas.axes.clear()
            self.ui3.PricePlot.canvas.axes.plot(price['date'], price['close'], color='blue', label='Actual Price')
            self.ui3.PricePlot.canvas.axes.plot(futures[0], futures[1], color='red', label='Future Price')
            self.ui3.PricePlot.canvas.axes.set_title('Prices Chart')
            self.ui3.PricePlot.canvas.axes.legend()
            self.ui3.PricePlot.canvas.draw()
        except:
            self._message('Invalid Ticker or date. It is also possible that provided data is '
                          'not sufficient for stock price prediction.','Warning')

    def PriceInInterval(self):
        global interval,futures
        future_periods = int(self.ui3.FuturePeriods.text())
        if isinstance(future_periods,int) and len(futures[1])>future_periods:
            self.ui3.FuturePrice.setText(str(futures[1][future_periods]))
        else:
            self._message('Next interval value should be integer not greater than 10% of shown stock price history',
                          'Information')


def main():
    global instrument_list, export_num, div_win
    instrument_list = []
    export_num = 0

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = FirstApp(MainWindow)
    MainWindow.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
