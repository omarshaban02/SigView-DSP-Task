PATH = 'signals/mitbih_train.csv'

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from SignalViewer import SignalViewerLogic
from PyQt5.QtCore import QTimer

import pyqtgraph as pg

import sys
from pathlib import Path
from res_rc import *  # Import the resource module

from PyQt5.uic import loadUiType
import urllib.request

import os
from os import path

ui, _ = loadUiType('main.ui')

class ShowHideCheckBoxes(QCheckBox):
    def __int__(self, parent):
        super().__init__(parent)
        QCheckBox.__init__(self)

class MainApp(QMainWindow, ui):
    _light_mode = True
    _play_pause_state1 = True
    _play_pause_state2 = True
    _play_pause_state3 = True

    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.resize(1200, 900)

        self.plot_widget1 = pg.PlotWidget(self.graphics_view1)
        self.graphics_view_layout1 = QHBoxLayout(self.graphics_view1)
        self.graphics_view_layout1.addWidget(self.plot_widget1)
        self.graphics_view1.setLayout(self.graphics_view_layout1)
        self.plot_widget1.setObjectName("plot_widget1")

        self.plot_widget2 = pg.PlotWidget(self.graphics_view2)
        self.graphics_view_layout2 = QHBoxLayout(self.graphics_view2)
        self.graphics_view_layout2.addWidget(self.plot_widget2)
        self.graphics_view2.setLayout(self.graphics_view_layout2)
        self.plot_widget2.setObjectName("plot_widget2")

        self.sv = SignalViewerLogic(self.plot_widget1)
        self.sv.load_dataset(PATH, 1)

        self.light_dark_mode_btn.clicked.connect(self.toggle_dark_light_mode)

        self.list_widget1 = self.table_of_signals1
        self.list_widget2 = self.table_of_signals2

        self.list_widget1.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list_widget2.setContextMenuPolicy(Qt.CustomContextMenu)

        self.list_widget1.customContextMenuRequested.connect(lambda pos: self.show_context_menu(pos, self.listWidget1))
        self.list_widget2.customContextMenuRequested.connect(lambda pos: self.show_context_menu(pos, self.listWidget2))

        # self.toggle_button.clicked.connect(self.slider)
        self.toggle_radioButton.clicked.connect(self.slider)


        self.play_pause_btn1.clicked.connect(self.toggle_play_pause_icon1)
        self.play_pause_btn2.clicked.connect(self.toggle_play_pause_icon2)
        self.play_pause_btn3.clicked.connect(self.toggle_play_pause_icon3)

    def show_context_menu(self, pos, list_widget):
        item = list_widget.itemAt(pos)

        if item:
            context_menu = QMenu()
            delete_action = QAction("Delete", self)
            delete_action.triggered.connect(lambda: self.deleteItem(item, list_widget))

            context_menu.addAction(delete_action)

            context_menu.exec_(list_widget.mapToGlobal(pos))

    def delete_item(self, item, list_widget):
        row = list_widget.row(item)
        list_widget.takeItem(row)

        # showHideCheckBox = showHideCheckBoxes(tableOfSignals1)
        # tableOfSignals1.setCellWidget(0, 1, showHideCheckBox)
        # for row_num in range(tableOfSignals_1.rowCount()):
        #     tableOfSignals_1.setCellWidget(0, row_num, showHideCheckBox)

    def toggle_dark_light_mode(self):

        if self._light_mode:
            self.setStyleSheet(Path('qss/darkStyle.qss').read_text())
            self.light_dark_mode_btn.setIcon(QIcon('icons/night-mode (1).png'))
            self._light_mode = False
        else:
            self.setStyleSheet(Path('qss/lightStyle.qss').read_text())
            self.light_dark_mode_btn.setIcon(QIcon('icons/sun.png'))
            self._light_mode = True



    def slider(self):
        if self.toggle_radioButton.isChecked():
            new_width = 60
            self.play_pause_btn1.setEnabled(False)
            self.rewind_btn1.setEnabled(False)
            self.stop_btn1.setEnabled(False)
            self.zoom_in_btn1.setEnabled(False)
            self.zoom_out_btn1.setEnabled(False)

            self.play_pause_btn2.setEnabled(False)
            self.rewind_btn2.setEnabled(False)
            self.stop_btn2.setEnabled(False)
            self.zoom_in_btn2.setEnabled(False)
            self.zoom_out_btn2.setEnabled(False)
        else:
            new_width = 0
            self.play_pause_btn1.setEnabled(True)
            self.rewind_btn1.setEnabled(True)
            self.stop_btn1.setEnabled(True)
            self.zoom_in_btn1.setEnabled(True)
            self.zoom_out_btn1.setEnabled(True)

            self.play_pause_btn2.setEnabled(True)
            self.rewind_btn2.setEnabled(True)
            self.stop_btn2.setEnabled(True)
            self.zoom_in_btn2.setEnabled(True)
            self.zoom_out_btn2.setEnabled(True)

        self.animation = QPropertyAnimation(self.left_side_bar, b"minimumWidth")
        self.animation.setDuration(40)
        self.animation.setEndValue(new_width)
        self.animation.setEasingCurve(QEasingCurve.InOutQuart)
        self.animation.start()
        # You may need to update the layout to see the change
        self.left_side_bar.update()

    def toggle_play_pause_icon1(self):
        if self._play_pause_state1:
            self.play_pause_btn1.setIcon(QIcon('icons/pause.png'))
            self._play_pause_state1 = False
        else:
            self.play_pause_btn1.setIcon(QIcon('icons/play-button.png'))
            self._play_pause_state1 = True

    def toggle_play_pause_icon2(self):
        if self._play_pause_state2:
            self.play_pause_btn2.setIcon(QIcon('icons/pause.png'))
            self._play_pause_state2 = False
        else:
            self.play_pause_btn2.setIcon(QIcon('icons/play-button.png'))
            self._play_pause_state2 = True

    def toggle_play_pause_icon3(self):
        if self._play_pause_state3:
            self.play_pause_btn3.setIcon(QIcon('icons/pause.png'))
            self._play_pause_state3 = False
        else:
            self.play_pause_btn3.setIcon(QIcon('icons/play-button.png'))
            self._play_pause_state3 = True



def main():
    app = QApplication(sys.argv)
    # app.setStyleSheet(Path('qss/lightStyle.qss').read_text())
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
