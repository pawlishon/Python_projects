from PyQt5.QtWidgets import QMessageBox, QDialog
from view.ta_win import *


class Technical_Analysis(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.bind_events()

    def bind_events(self):
        self.ui.lineEditA1.setEnabled(False)
        self.ui.lineEditA2.setEnabled(False)