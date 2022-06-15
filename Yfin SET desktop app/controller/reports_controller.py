from view.ReportsDialog import *
from PyQt5.QtWidgets import QMessageBox, QDialog
import pandas as pd
from helpers.pandas_model import pandasModel
from model.financial_statements import get_financial_statements


class FinancialReports(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.report1 = pd.DataFrame()
        self.report2 = pd.DataFrame()
        self.bind_events()

    def bind_events(self):
        self.ui.reportButton_3.clicked.connect(self.report_1)
        self.ui.reportButton_4.clicked.connect(self.report_2)
        self.ui.comboBoxTickers_2.addItem('Ticker 1')
        self.ui.comboBoxTickers_2.addItem('Ticker 2')
        self.ui.comboBoxTickers_2.addItem('Both')
        self._possible_features = ['researchDevelopment', 'incomeBeforeTax', 'netIncome',
                                   'sellingGeneralAdministrative', 'grossProfit', 'operatingIncome', 'interestExpense',
                                   'totalRevenue', 'costOfRevenue', 'grossProfitMargin', 'taxPaid', 'netRatio',
                                   'totalLiab', 'totalStockholderEquity', 'totalAssets', 'commonStock',
                                   'otherCurrentAssets', 'retainedEarnings', 'treasuryStock', 'cash',
                                   'totalCurrentLiabilities', 'shortLongTermDebt', 'propertyPlantEquipment',
                                   'totalCurrentAssets', 'netTangibleAssets', 'shortTermInvestments', 'netReceivables',
                                   'longTermDebt', 'inventory', 'currentRatio', 'debtToESRatio', 'longOverShortDebt',
                                   'depreciation', 'capitalExpenditures', 'returnOnShareholdersEquity']
        for i in self._possible_features:
            self.ui.comboBoxFeatures_2.addItem(i)
        self.ui.plotButton_2.clicked.connect(self.plot_features)

    def report_1(self):
        try:
            ticker = self.ui.tickerInput1_2.text()
            self.ui.t1_Label.setText(ticker.upper()+' (values in millions): ')
            self.report1, self.ratios1 = get_financial_statements(ticker)
            model = pandasModel(self.report1)
            model2 = pandasModel(self.ratios1)
            self.ui.reportView1.setModel(model)
            self.ui.reportView1_2.setModel(model2)
        except:
            self._message('Invalid ticker or no data for this identifier.', 'Information')

    def report_2(self):
        try:
            ticker = self.ui.tickerInput2_2.text()
            self.ui.t2_Label.setText(ticker.upper() + ' (values in millions): ')
            self.report2, self.ratios2 = get_financial_statements(ticker)
            model = pandasModel(self.report2)
            model2 = pandasModel(self.ratios2)
            self.ui.reportView2.setModel(model)
            self.ui.reportView2_2.setModel(model2)
        except:
            self._message('Invalid ticker or no data for this identifier.', 'Information')

    def _message(self, text, title):
        msg = QMessageBox()
        msg.setText(text)
        msg.setWindowTitle(title)
        msg.exec_()

    def plot_features(self):
        ticker_option = str(self.ui.comboBoxTickers_2.currentText())
        feature_option = str(self.ui.comboBoxFeatures_2.currentText())
        self.ui.plotArea_2.canvas.axes.clear()
        if ticker_option == 'Ticker 1':
            if len(self.report1)!=0:
                join_table = pd.concat([self.report1, self.ratios1])
                x = join_table.columns.to_list()[1:]
                y = join_table.loc[join_table['Breakdown'] == feature_option].values.tolist()[0][1:]
                self.ui.plotArea_2.canvas.axes.plot(list(reversed(x)), list(reversed(y)))
                self.ui.plotArea_2.canvas.axes.set_title('Feature Chart')
                self.ui.plotArea_2.canvas.draw()
            else:
                self._message('Please get the report for Ticker 1.', 'Information')
        elif ticker_option == 'Ticker 2':
            if len(self.report2) != 0:
                join_table = pd.concat([self.report2, self.ratios2])
                x = join_table.columns.to_list()[1:]
                y = join_table.loc[join_table['Breakdown'] == feature_option].values.tolist()[0][1:]
                self.ui.plotArea_2.canvas.axes.plot(list(reversed(x)), list(reversed(y)))
                self.ui.plotArea_2.canvas.axes.set_title('Feature Chart')
                self.ui.plotArea_2.canvas.draw()
            else:
                self._message('Please get the report for Ticker 2.', 'Information')
        else:
            if len(self.report1)!=0 and len(self.report2)!=0:
                join_table1 = pd.concat([self.report1, self.ratios1])
                join_table2 = pd.concat([self.report2, self.ratios2])
                self.ui.plotArea_2.canvas.axes.clear()
                x1 = join_table1.columns.to_list()[1:]
                y1 = join_table1.loc[join_table1['Breakdown'] == feature_option].values.tolist()[0][1:]
                y2 = join_table2.loc[join_table2['Breakdown'] == feature_option].values.tolist()[0][1:]
                self.ui.plotArea_2.canvas.axes.plot(list(reversed(x1)), list(reversed(y1)), color='blue',
                                                    label='First Ticker')
                self.ui.plotArea_2.canvas.axes.plot(list(reversed(x1)), list(reversed(y2)), color='red', label='Second Ticker')
                self.ui.plotArea_2.canvas.axes.set_title('Feature Chart')
                self.ui.plotArea_2.canvas.axes.legend()
                self.ui.plotArea_2.canvas.draw()
            else:
                self._message('Please get the reports for both tickers.', 'Information')