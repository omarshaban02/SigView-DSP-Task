from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
from pathlib import Path
from res_rc import *  # Import the resource module

from PyQt5.uic import loadUiType
import urllib.request

import os
from os import path



ui, _ = loadUiType('main.ui')


class showHideComboBoxes(QComboBox):
    def _init__(self, parent):
        super().__init__(parent)
        self.addItems(['Blue', 'Red', 'Green'])
        self.currentIndexChanged.connect(self.getComboValue)

    def getComboValue(self):
        print(self.currentText())
        # return self.currentText()


class MainApp(QMainWindow, ui):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)

        lightDarkModeButton = self.lightDarkModePushButton
        lightDarkModeButton.setCheckable(True)
        lightDarkModeButton.clicked.connect(self.toggleDarkLightMode)


        showHideComboBox = showHideComboBoxes(self)

        tableOfSignals_1 = self.tableOfSignals_1
        for row_num in range(tableOfSignals_1.rowCount()):
            tableOfSignals_1.setCellWidget(0, row_num, showHideComboBox)

    def toggleDarkLightMode(self, checked):
        # print("Done")
        if checked:
            self.setStyleSheet(Path('qss/darkStyle.qss').read_text())
            #icon
        else:
            self.setStyleSheet(Path('qss/lightStyle.qss').read_text())
            #icon




def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(Path('qss/lightStyle.qss').read_text())
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
