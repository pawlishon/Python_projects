from PyQt5.QtWidgets import QMessageBox, QDialog
from view.Dividends_dialog import *
import yahoo_fin.stock_info as si
from helpers.pandas_model import pandasModel
import traceback
from matplotlib.ticker import MaxNLocator


class DividendHistory(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.bind_events()

    def bind_events(self):
        self.ui.ShowDiv.clicked.connect(self.DHis)


    def _message(self, text, title):
        msg = QMessageBox()
        msg.setText(text)
        msg.setWindowTitle(title)
        msg.exec_()

    def DHis(self):
        ticker = self.ui.DivTicker.text()
        start_date = self.ui.DivDate.date().toPyDate().strftime('%d-%m-%Y')
        try:
            data = si.get_dividends(ticker, start_date)
            data = data.reset_index()
            data.columns = ['Date', 'Amount USD', 'Ticker']
            data['Date'] = data['Date'].dt.strftime('%d-%b-%Y')
            data = data.drop('Ticker', axis=1)
            model = pandasModel(data)
            self.ui.DivView.setModel(model)
            self.ui.DivPlot.canvas.axes.clear()
            self.ui.DivPlot.canvas.axes.plot(data['Date'], data['Amount USD'])
            self.ui.DivPlot.canvas.axes.set_title('Dividends Chart')
            self.ui.DivPlot.canvas.axes.xaxis.set_major_locator(MaxNLocator(6))
            #self.ui.DivPlot.canvas.axes.tick_params(axis='x', labelrotation=-45)
            self.ui.DivPlot.canvas.draw()
        except:
            self._message(traceback.format_exc(), 'Information')
