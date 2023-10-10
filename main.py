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


class showHideCheckBoxes(QCheckBox):
    def __int__(self, parent):
        super().__init__(parent)
        QCheckBox.__init__(self)


class MainApp(QMainWindow, ui):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.resize(1200, 900)

        lightDarkModeButton = self.lightDarkModePushButton
        lightDarkModeButton.setCheckable(True)
        lightDarkModeButton.clicked.connect(self.toggleDarkLightMode)



        self.listWidget1 = self.tableOfSignals_1
        self.listWidget2 = self.tableOfSignals_2

        self.listWidget1.setContextMenuPolicy(Qt.CustomContextMenu)
        self.listWidget2.setContextMenuPolicy(Qt.CustomContextMenu)

        self.listWidget1.customContextMenuRequested.connect(lambda pos: self.showContextMenu(pos, self.listWidget1))
        self.listWidget2.customContextMenuRequested.connect(lambda pos: self.showContextMenu(pos, self.listWidget2))

    def showContextMenu(self, pos, list_widget):
        item = list_widget.itemAt(pos)

        if item:
            context_menu = QMenu()
            delete_action = QAction("Delete", self)
            delete_action.triggered.connect(lambda: self.deleteItem(item, list_widget))

            context_menu.addAction(delete_action)

            context_menu.exec_(list_widget.mapToGlobal(pos))

    def deleteItem(self, item, list_widget):
        row = list_widget.row(item)
        list_widget.takeItem(row)

        # showHideCheckBox = showHideCheckBoxes(tableOfSignals1)
        # tableOfSignals1.setCellWidget(0, 1, showHideCheckBox)
        # for row_num in range(tableOfSignals_1.rowCount()):
        #     tableOfSignals_1.setCellWidget(0, row_num, showHideCheckBox)

    def toggleDarkLightMode(self, checked):
        # print("Done")
        if checked:
            self.setStyleSheet(Path('qss/darkStyle.qss').read_text())
            # icon
        else:
            self.setStyleSheet(Path('qss/lightStyle.qss').read_text())
            # icon


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(Path('qss/lightStyle.qss').read_text())
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
