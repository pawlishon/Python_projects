import sys
from view.MainWindow import *
import os


class MenuController(Ui_MainWindow):
    def __init__(self, window):
        self.setupUi(window)
        window.setWindowTitle('Tool for stock evaluation - by Pawel Piatkowski')
        self.bind_events()

    def bind_events(self):
        # self.actionPrice_History.triggered.connect(self._clicked_show_price_history)
        # self.actionReport_Analysis.triggered.connect(self._clicked_show_report_analysis)
        # self.actionCandlestick_pattern_recognition.triggered.connect(self._clicked_show_pattern_recognition)
        self.actionStock_Ratios.triggered.connect(self._clicked_show_stock_ratios)
        # self.actionTicker_dividend_history.triggered.connect(self._clicked_show_dividend_history)
        # self.actionValuation_of_Stock_price.triggered.connect(self._clicked_show_valuation_of_stock)
        # self.actionRatio_Explanation.triggered.connect(self._clicked_show_ratio_explanation)
        # self.actionManual_in_Polish.triggered.connect(self._clicked_show_manual)

    def _clicked_show_stock_ratios(self):
        from controller.stock_ratios import StockRatios
        stock_ratios_controller = StockRatios()
        stock_ratios_controller.exec_()

def main():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = MenuController(MainWindow)
    MainWindow.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    if '_PYIBoot_SPLASH' in os.environ and importlib.util.find_spec("pyi_splash"):
        import pyi_splash #It may show an error in your IDE but it's fine
        pyi_splash.update_text('UI Loaded ...')
        pyi_splash.close()
    main()
