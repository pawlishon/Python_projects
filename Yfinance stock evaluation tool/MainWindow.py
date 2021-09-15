# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1161, 814)
        MainWindow.setStyleSheet("background-color: qconicalgradient(cx:0, cy:0, angle:135, stop:0 rgba(255, 255, 0, 69), stop:0.375 rgba(255, 255, 0, 69), stop:0.423533 rgba(251, 255, 0, 145), stop:0.45 rgba(247, 255, 0, 208), stop:0.477581 rgba(255, 244, 71, 130), stop:0.518717 rgba(255, 218, 71, 130), stop:0.55 rgba(255, 255, 0, 255), stop:0.57754 rgba(255, 203, 0, 130), stop:0.625 rgba(255, 255, 0, 69), stop:1 rgba(255, 255, 0, 69));")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.AddTicker = QtWidgets.QCommandLinkButton(self.centralwidget)
        self.AddTicker.setGeometry(QtCore.QRect(250, 60, 131, 41))
        self.AddTicker.setStyleSheet("\n"
"\n"
"background-color: rgb(0, 170, 255);")
        self.AddTicker.setObjectName("AddTicker")
        self.InsertField = QtWidgets.QLineEdit(self.centralwidget)
        self.InsertField.setGeometry(QtCore.QRect(90, 60, 151, 31))
        self.InsertField.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.InsertField.setObjectName("InsertField")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(420, 30, 311, 231))
        self.textBrowser.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 12pt \"MS Shell Dlg 2\";")
        self.textBrowser.setObjectName("textBrowser")
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(30, 270, 1041, 401))
        self.tableView.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.tableView.setObjectName("tableView")
        self.EvaluateButton = QtWidgets.QPushButton(self.centralwidget)
        self.EvaluateButton.setGeometry(QtCore.QRect(60, 120, 201, 41))
        self.EvaluateButton.setStyleSheet("background-color: rgb(0, 170, 255);\n"
"font: 14pt \"MS Shell Dlg 2\";")
        self.EvaluateButton.setObjectName("EvaluateButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 10, 311, 31))
        self.label.setStyleSheet("font: 14pt \"MS Shell Dlg 2\";")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 60, 71, 31))
        self.label_2.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";")
        self.label_2.setObjectName("label_2")
        self.EvaluationProgress = QtWidgets.QProgressBar(self.centralwidget)
        self.EvaluationProgress.setGeometry(QtCore.QRect(290, 130, 118, 23))
        self.EvaluationProgress.setProperty("value", 24)
        self.EvaluationProgress.setObjectName("EvaluationProgress")
        self.ExportButton = QtWidgets.QPushButton(self.centralwidget)
        self.ExportButton.setGeometry(QtCore.QRect(60, 180, 201, 41))
        self.ExportButton.setStyleSheet("background-color: rgb(0, 170, 255);\n"
"font: 14pt \"MS Shell Dlg 2\";")
        self.ExportButton.setObjectName("ExportButton")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(430, 0, 301, 21))
        self.label_3.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";")
        self.label_3.setObjectName("label_3")
        self.ClearButton = QtWidgets.QPushButton(self.centralwidget)
        self.ClearButton.setGeometry(QtCore.QRect(740, 30, 201, 41))
        self.ClearButton.setStyleSheet("background-color: rgb(0, 170, 255);\n"
"font: 14pt \"MS Shell Dlg 2\";")
        self.ClearButton.setObjectName("ClearButton")
        self.RemoveLastButton = QtWidgets.QPushButton(self.centralwidget)
        self.RemoveLastButton.setGeometry(QtCore.QRect(740, 80, 201, 41))
        self.RemoveLastButton.setStyleSheet("background-color: rgb(0, 170, 255);\n"
"font: 14pt \"MS Shell Dlg 2\";")
        self.RemoveLastButton.setObjectName("RemoveLastButton")
        self.ForecastButton = QtWidgets.QPushButton(self.centralwidget)
        self.ForecastButton.setGeometry(QtCore.QRect(30, 680, 201, 41))
        self.ForecastButton.setStyleSheet("\n"
"background-color: rgb(85, 255, 0);\n"
"font: 14pt \"MS Shell Dlg 2\";")
        self.ForecastButton.setObjectName("ForecastButton")
        self.WikiButton = QtWidgets.QPushButton(self.centralwidget)
        self.WikiButton.setGeometry(QtCore.QRect(240, 680, 201, 41))
        self.WikiButton.setStyleSheet("background-color: rgb(85, 255, 0);\n"
"font: 14pt \"MS Shell Dlg 2\";")
        self.WikiButton.setObjectName("WikiButton")
        self.DirectoryPath = QtWidgets.QLineEdit(self.centralwidget)
        self.DirectoryPath.setGeometry(QtCore.QRect(740, 210, 231, 41))
        self.DirectoryPath.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.DirectoryPath.setObjectName("DirectoryPath")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(740, 140, 301, 21))
        self.label_4.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";")
        self.label_4.setObjectName("label_4")
        self.ImportButton = QtWidgets.QPushButton(self.centralwidget)
        self.ImportButton.setGeometry(QtCore.QRect(1070, 210, 81, 41))
        self.ImportButton.setStyleSheet("background-color: rgb(0, 170, 255);\n"
"font: 10pt \"MS Shell Dlg 2\";\n"
"")
        self.ImportButton.setObjectName("ImportButton")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(740, 180, 241, 16))
        self.label_5.setStyleSheet("font: 10pt \"MS Shell Dlg 2\";")
        self.label_5.setObjectName("label_5")
        self.DivButton = QtWidgets.QPushButton(self.centralwidget)
        self.DivButton.setGeometry(QtCore.QRect(450, 680, 201, 41))
        self.DivButton.setStyleSheet("background-color: rgb(85, 255, 0);\n"
"font: 14pt \"MS Shell Dlg 2\";")
        self.DivButton.setObjectName("DivButton")
        self.DowButton = QtWidgets.QPushButton(self.centralwidget)
        self.DowButton.setGeometry(QtCore.QRect(960, 30, 201, 41))
        self.DowButton.setStyleSheet("background-color: rgb(0, 255, 255);\n"
"font: 14pt \"MS Shell Dlg 2\";")
        self.DowButton.setObjectName("DowButton")
        self.SPButton = QtWidgets.QPushButton(self.centralwidget)
        self.SPButton.setGeometry(QtCore.QRect(960, 80, 201, 41))
        self.SPButton.setStyleSheet("background-color: rgb(0, 255, 255);\n"
"font: 14pt \"MS Shell Dlg 2\";")
        self.SPButton.setObjectName("SPButton")
        self.BrowseButton = QtWidgets.QPushButton(self.centralwidget)
        self.BrowseButton.setGeometry(QtCore.QRect(980, 210, 81, 41))
        self.BrowseButton.setStyleSheet("background-color: rgb(0, 170, 255);\n"
"font: 10pt \"MS Shell Dlg 2\";\n"
"")
        self.BrowseButton.setObjectName("BrowseButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1161, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.AddTicker.setText(_translate("MainWindow", "Insert "))
        self.EvaluateButton.setText(_translate("MainWindow", "Evaluate"))
        self.label.setText(_translate("MainWindow", "Tool for stock evaluation"))
        self.label_2.setText(_translate("MainWindow", "Ticker:"))
        self.ExportButton.setText(_translate("MainWindow", "Export to excel"))
        self.label_3.setText(_translate("MainWindow", "Current instrument list:"))
        self.ClearButton.setText(_translate("MainWindow", "Clear list"))
        self.RemoveLastButton.setText(_translate("MainWindow", "Remove last"))
        self.ForecastButton.setText(_translate("MainWindow", "Forecast"))
        self.WikiButton.setText(_translate("MainWindow", "Ratio explanation"))
        self.label_4.setText(_translate("MainWindow", "Import tickers from csv file:"))
        self.ImportButton.setText(_translate("MainWindow", "Add tickers"))
        self.label_5.setText(_translate("MainWindow", "Please provide csv file directory"))
        self.DivButton.setText(_translate("MainWindow", "Dividends history"))
        self.DowButton.setText(_translate("MainWindow", "Import Dow list"))
        self.SPButton.setText(_translate("MainWindow", "Import SP500 list"))
        self.BrowseButton.setText(_translate("MainWindow", "Browse..."))
