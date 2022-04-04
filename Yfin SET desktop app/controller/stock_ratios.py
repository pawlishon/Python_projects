from PyQt5.QtWidgets import QMessageBox, QDialog
from view.stock_evaluation import *
import pandas as pd
from PyQt5.QtCore import QThreadPool
from helpers.PyQTWorker import *
from model.evaluation import my_valuation
from helpers.pandas_model import pandasModel
from helpers.file_dialog import App
import yahoo_fin.stock_info as si
import csv
from datetime import date


class StockRatios(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.bind_events()
        self.instrument_list = []
        self.Final_df = pd.DataFrame()
        self.export_number = 0
        self.threadpool = QThreadPool()

    def bind_events(self):
        self.ui.AddTicker.clicked.connect(self.showInstrument)
        self.ui.EvaluateButton.clicked.connect(self.thread)
        self.ui.ClearButton.clicked.connect(self.ClearContent)
        self.ui.ExportButton.clicked.connect(self.ExportContent)
        self.ui.EvaluationProgress.setValue(0)
        self.ui.RemoveLastButton.clicked.connect(self.Removal)
        self.ui.ImportButton.clicked.connect(self.ImportData)
        self.ui.DowButton.clicked.connect(self.ImportDow)
        self.ui.SPButton.clicked.connect(self.ImportSP)
        self.ui.BrowseButton.clicked.connect(self.BrowseFiles)

    def thread(self):
        self.ui.EvaluateButton.setEnabled(False)
        worker = Worker(self.Evaluate)
        worker.signals.result.connect(self.show_table)
        worker.signals.progress.connect(self.progress_fn)
        self.threadpool.start(worker)

    def showInstrument(self):
        self.instrument_list.append(self.ui.InsertField.text())
        string = ''
        for item in self.instrument_list:
            if string == '':
                string = item + ', '
            else:
                string = string + item + ', '
        self.ui.textBrowser.setText(string)

    def Evaluate(self, progress_callback):
        self.Final_df = pd.DataFrame()
        i = 0
        for ticker in self.instrument_list:
            temp = my_valuation(ticker)
            self.Final_df = pd.concat([self.Final_df, temp], axis=0)
            i = i + 1
            progress_callback.emit(int(i/len(self.instrument_list) * 100))
        return self.Final_df

    def progress_fn(self, n):
        self.ui.EvaluationProgress.setValue(n)

    def show_table(self, data):
        model = pandasModel(data)
        self.ui.tableView.setModel(model)
        self.ui.EvaluateButton.setEnabled(True)

    def ClearContent(self):
        self.instrument_list = []
        self.ui.textBrowser.setText('')

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
        self.ui.textBrowser.setText(string)

    def _message(self, text, title):
        msg = QMessageBox()
        msg.setText(text)
        msg.setWindowTitle(title)
        msg.exec_()

    def ImportData(self):
        path = self.ui.DirectoryPath.text()
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
                self.ui.textBrowser.setText(string)
            except:
                self._message('Invalid file format. Csv file should contain one column with header. '
                              'This column should have Yahoo finance tickers.', 'Warning')
        else:
            self._message('It is not a csv file !', 'Warning')

    def BrowseFiles(self):
        self._shared_memory = {}
        self.ex = App(self._shared_memory)
        self.ui.DirectoryPath.setText(self._shared_memory.get('filename'))

    def ImportDow(self):
        self.instrument_list = self.instrument_list + si.tickers_dow()
        string = ''
        for item in self.instrument_list:
            if string == '':
                string = item + ', '
            else:
                string = string + item + ', '
        self.ui.textBrowser.setText(string)

    def ImportSP(self):
        self.instrument_list = self.instrument_list + si.tickers_sp500()
        string = ''
        for item in self.instrument_list:
            if string == '':
                string = item + ', '
            else:
                string = string + item + ', '
        self.ui.textBrowser.setText(string)

    def ExportToExcel(self,instrument_results):
        self.export_number = self.export_number + 1
        instrument_results.to_excel('results_' + str(date.today()) + '_' + str(self.export_number) + '.xlsx', index=False)