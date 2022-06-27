from PyQt5.QtWidgets import QMessageBox, QDialog
from view.ta_win import *
from model.technical_analysis import plot_ta

class Technical_Analysis(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.bind_events()

    def bind_events(self):
        self.ui.lineEditA1.setEnabled(False)
        self.ui.lineEditA2.setEnabled(False)
        self.ui.checkBoxMA.stateChanged.connect(self.enable_avg)
        self.ui.dateEditEnd.setDateTime(QtCore.QDateTime.currentDateTime())
        self.ui.pushButton.clicked.connect(self.show_plot)

    def enable_avg(self):
        if self.ui.checkBoxMA.isChecked():
            self.ui.lineEditA1.setEnabled(True)
            self.ui.lineEditA2.setEnabled(True)
        else:
            self.ui.lineEditA1.setEnabled(False)
            self.ui.lineEditA2.setEnabled(False)

    def show_plot(self):
        ticker = self.ui.tickerEdit.text()
        start_date = self.ui.dateEditStart.date().toPyDate().strftime('%Y-%m-%d')
        end_date = self.ui.dateEditEnd.date().toPyDate().strftime('%Y-%m-%d')
        vol = False
        bb = False
        ma = False
        pattern = False
        rsi = False
        short = 10
        long = 50
        if self.ui.checkBoxVol.isChecked():
            vol = True
        if self.ui.checkBoxMA.isChecked():
            ma = True
            short = int(self.ui.lineEditA1.text())
            long = int(self.ui.lineEditA2.text())
        if self.ui.checkBoxBB.isChecked():
            bb = True
        if self.ui.checkBoxPR.isChecked():
            pattern = True
        if self.ui.checkBoxRSI.isChecked():
            rsi = True
        plot_ta(ticker, start_date, end_date, bb, rsi, ma, vol, pattern, short, long)
