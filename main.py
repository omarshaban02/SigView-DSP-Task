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



    light_mode = True
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.resize(1200, 900)

        # self.graphicsView = Plotwidget(self.centralwidget)
        # self.graphicsView.setGeometry(QtCore.Qrect(60, 40, 681, 281))
        # self.graphicsView.setObjectName("graphicsview")
        # self.graphicsView_2 = Plotwidget(self.centralwidget)
        # self.graphicsView_2.setGeometry(QtCore.Qrect(60, 40, 681, 281))
        # self.graphicsView_2.setObjectName("graphicsview_2")

        self.light_dark_mode_btn.clicked.connect(self.toggleDarkLightMode)

        self.listWidget1 = self.tableOfSignals_1
        self.listWidget2 = self.tableOfSignals_2

        self.listWidget1.setContextMenuPolicy(Qt.CustomContextMenu)
        self.listWidget2.setContextMenuPolicy(Qt.CustomContextMenu)

        self.listWidget1.customContextMenuRequested.connect(lambda pos: self.showContextMenu(pos, self.listWidget1))
        self.listWidget2.customContextMenuRequested.connect(lambda pos: self.showContextMenu(pos, self.listWidget2))

        self.toggle_button.clicked.connect(self.slider)

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

    def toggleDarkLightMode(self):

        if self.light_mode:
            self.setStyleSheet(Path('qss/darkStyle.qss').read_text())
            self.light_dark_mode_btn.setIcon(QIcon('icons/night-mode (1).png'))
            self.light_mode = False
        else:
            self.setStyleSheet(Path('qss/lightStyle.qss').read_text())
            self.light_dark_mode_btn.setIcon(QIcon('icons/sun.png'))
            self.light_mode = True


    def slider(self):
        width = self.left_side_bar.width()
        if width == 0:
            newWidth = 50
        else:
            newWidth = 0




        self.animation = QPropertyAnimation(self.left_side_bar, b"minimumWidth")
        self.animation.setDuration(40)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        self.animation.setEasingCurve(QEasingCurve.InOutQuart)
        self.animation.start()

        # You may need to update the layout to see the change
        self.left_side_bar.update()


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(Path('qss/lightStyle.qss').read_text())
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
