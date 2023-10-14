PATH = 'signals/mitbih_train.csv'

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from SignalViewer import SignalViewerLogic, Signal
from PyQt5.QtCore import QTimer

import pyqtgraph as pg

import pandas as pd

import sys
from pathlib import Path
from res_rc import *  # Import the resource module

from PyQt5.uic import loadUiType
import urllib.request

import os
from os import path
import random

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
    _signal1_is_hide = False
    _signal2_is_hide = False
    _previous_horizontal_scrollBar_value1 = 0
    _previous_vertical_scrollBar_value1 = 0
    _previous_horizontal_scrollBar_value2 = 0
    _previous_vertical_scrollBar_value2 = 0

    def delete_item(self, item, list_widget):
        row = list_widget.row(item)
        list_widget.takeItem(row)

        # showHideCheckBox = showHideCheckBoxes(tableOfSignals1)
        # tableOfSignals1.setCellWidget(0, 1, showHideCheckBox)
        # for row_num in range(tableOfSignals_1.rowCount()):
        #     tableOfSignals_1.setCellWidget(0, row_num, showHideCheckBox)

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
        self.sv2 = SignalViewerLogic(self.plot_widget2)
        # self.horizontal_scrollBar1.setMinimum(0)
        # self.horizontal_scrollBar1.setMaximum(150)
        # self.sv.xScrollBar = self.horizontal_scrollBar1
        # self.sv2.xScrollBar = self.horizontal_scrollBar2

        self.light_dark_mode_btn.clicked.connect(self.toggle_dark_light_mode)

        self.list_widget1 = self.signals_list1
        self.list_widget2 = self.signals_list2

        self.list_widget1.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list_widget2.setContextMenuPolicy(Qt.CustomContextMenu)

        self.list_widget1.customContextMenuRequested.connect(lambda pos: self.show_context_menu(pos, self.listWidget1))
        self.list_widget2.customContextMenuRequested.connect(lambda pos: self.show_context_menu(pos, self.listWidget2))

        self.toggle_radioButton.clicked.connect(self.slider)

        #connect the scrollBar with QGraph
        self.horizontal_scrollBar1.valueChanged.connect(self.link_horizontal_scrollBar_with_Graph1)
        self.vertical_scrollBar1.valueChanged.connect(self.link_vertical_scrollBar_with_Graph1)
        self.horizontal_scrollBar2.valueChanged.connect(self.link_horizontal_scrollBar_with_Graph2)
        self.vertical_scrollBar2.valueChanged.connect(self.link_vertical_scrollBar_with_Graph2)

        # 1st graphics_view buttons
        self.open_btn1.clicked.connect(lambda list_widget: self.openCSV1(self.list_widget1))
        self.plot_btn1.clicked.connect(self.add_signal_to_graph1)
        self.replay_btn1.clicked.connect(self.replay_active_signal1)
        self.stop_btn1.clicked.connect(self.stop_active_signal1)
        self.reset_view_btn1.clicked.connect(self.reset_view1)
        self.hide_btn1.clicked.connect(self.remove_active_signal1)# head not clear or remove
        self.move_down_btn.clicked.connect(self.move_active_signal1_to_graph2)

        # 2nd graphics_view buttons
        self.open_btn2.clicked.connect(lambda list_widget: self.openCSV2(self.list_widget2))
        self.plot_btn2.clicked.connect(self.add_signal_to_graph2)
        self.replay_btn2.clicked.connect(self.replay_active_signal2)
        self.stop_btn2.clicked.connect(self.stop_active_signal2)
        self.reset_view_btn2.clicked.connect(self.reset_view2)
        self.hide_btn2.clicked.connect(self.remove_active_signal2)
        self.move_up_btn.clicked.connect(self.move_active_signal2_to_graph1)

        # synchronous graphics_view
        self.replay_btn3.clicked.connect(self.replay_active_synchronous_signals)
        self.stop_btn3.clicked.connect(self.stop_active_synchronous_signals)
        self.reset_view_btn3.clicked.connect(self.reset_synchronous_views)
        self.hide_btn3.clicked.connect(self.remove_active_synchronous_signals)

        #for all play, pause buttons
        self.play_pause_btn1.clicked.connect(self.toggle_play_pause_icon1)
        self.play_pause_btn2.clicked.connect(self.toggle_play_pause_icon2)
        self.play_pause_btn3.clicked.connect(self.toggle_play_pause_icon3)

        self.color_comboBox1.currentTextChanged.connect(lambda signals_list: self.change_color(self.sv.active_signals, self.color_comboBox1.currentText().lower()))
        self.color_comboBox2.currentTextChanged.connect(lambda signals_list:self.change_color(self.sv2.active_signals, self.color_comboBox2.currentText().lower()))

        self.speedDoubleSpinBox_1.valueChanged.connect(lambda graph: self.change_speed(self.sv,self.speedDoubleSpinBox_1.value()))
        self.speedDoubleSpinBox_2.valueChanged.connect(lambda graph: self.change_speed(self.sv2, self.speedDoubleSpinBox_2.value()))

        self.color_dict = {
            'red': (255, 0, 0),
            'green': (0, 255, 0),
            'blue': (0, 0, 255),
            'orange': (255, 165, 0),
            'purple': (128, 0, 128),
            'pink': (255, 192, 203),
            'yellow': (255, 255, 0),
            'brown': (139, 69, 19),
            'black': (0, 0, 0),
            'white': (255, 255, 255),
            'navy': (0, 0, 128),
            'magenta': (255, 0, 255),
            'violet': (238, 130, 238),
            'indigo': (75, 0, 130),
            'lime': (0, 255, 0),
            'cyan': (0, 255, 255),
            'gold': (255, 215, 0),
            'maroon': (128, 0, 0),
            'gray': (128, 128, 128),
            'silver': (192, 192,192)
        }

    def show_context_menu(self, pos, list_widget):
        item = list_widget.itemAt(pos)
        if item:
            context_menu = QMenu()
            delete_action = QAction("Delete", self)
            delete_action.triggered.connect(lambda: self.deleteItem(item, list_widget))
            context_menu.addAction(delete_action)
            context_menu.exec_(list_widget.mapToGlobal(pos))

    def toggle_dark_light_mode(self):
        if self._light_mode:
            self.setStyleSheet(Path('qss/darkStyle.qss').read_text())
            self.sv.background_color = (25, 35, 45)
            self.sv2.background_color = (25, 35, 45)
            self.light_dark_mode_btn.setIcon(QIcon('icons/moon.svg'))
            self._light_mode = False
        else:
            self.setStyleSheet(Path('qss/lightStyle.qss').read_text())
            self.sv.background_color = (255, 255, 255)
            self.sv2.background_color = (255, 255, 255)
            self.light_dark_mode_btn.setIcon(QIcon('icons/brightness.svg'))
            self._light_mode = True

    def slider(self):
        self.sv.pause()
        self.sv2.pause()
        if self.toggle_radioButton.isChecked():
            #for change icons
            self.play_pause_btn1.setIcon(QIcon('icons/play.svg'))
            self._play_pause_state1 = False
            self.play_pause_btn2.setIcon(QIcon('icons/play.svg'))
            self._play_pause_state2 = False

            # for slide slider and disable the other buttons
            new_width = 60
            self.play_pause_btn1.setEnabled(False)
            self.replay_btn1.setEnabled(False)
            self.stop_btn1.setEnabled(False)
            self.reset_view_btn1.setEnabled(False)
            self.hide_btn1.setEnabled(False)
            self.move_up_btn.setEnabled(False)
            
            self.play_pause_btn2.setEnabled(False)
            self.replay_btn2.setEnabled(False)
            self.stop_btn2.setEnabled(False)
            self.reset_view_btn2.setEnabled(False)
            self.hide_btn2.setEnabled(False)
            self.move_down_btn.setEnabled(False)
        else:
            self._play_pause_state1 = True
            self._play_pause_state2 = True

            new_width = 0
            self.play_pause_btn1.setEnabled(True)
            self.replay_btn1.setEnabled(True)
            self.stop_btn1.setEnabled(True)
            self.reset_view_btn1.setEnabled(True)
            self.hide_btn1.setEnabled(True)
            self.move_up_btn.setEnabled(True)

            self.play_pause_btn2.setEnabled(True)
            self.replay_btn2.setEnabled(True)
            self.stop_btn2.setEnabled(True)
            self.reset_view_btn2.setEnabled(True)
            self.hide_btn2.setEnabled(True)
            self.move_down_btn.setEnabled(True)

        self.animation = QPropertyAnimation(self.left_side_bar, b"minimumWidth")
        self.animation.setDuration(40)
        self.animation.setEndValue(new_width)
        self.animation.setEasingCurve(QEasingCurve.InOutQuart)
        self.animation.start()
        self.left_side_bar.update()

    def toggle_play_pause_icon1(self):
        if self._play_pause_state1:
            self.sv.play()
            self.play_pause_btn1.setIcon(QIcon('icons/pause.svg'))
            self._play_pause_state1 = False
        else:
            self.sv.pause()
            self.play_pause_btn1.setIcon(QIcon('icons/play.svg'))
            self._play_pause_state1 = True

    def link_horizontal_scrollBar_with_Graph1(self, value):
        if value == 0:
            self.sv.home_view()
        else:
            delta = value - self._previous_horizontal_scrollBar_value1
            self._previous_horizontal_scrollBar_value1 = value  # Update the previous value
            if delta > 0:
                # Scroll to the right
                self.sv.horizontal_shift(1)
            elif delta < 0:
                # Scroll to the left
                self.sv.horizontal_shift(-1)

    def link_vertical_scrollBar_with_Graph1(self, value):
        if value == 0:
            self.sv.home_view()
        else:
            delta = value - self._previous_vertical_scrollBar_value1
            self._previous_vertical_scrollBar_value1 = value  # Update the previous value
            if delta > 0:
                # Scroll to the right
                self.sv.vertical_shift(1)
            elif delta < 0:
                # Scroll to the left
                self.sv.vertical_shift(-1)

    def link_horizontal_scrollBar_with_Graph2(self, value):
        if value == 0:
            self.sv2.home_view()
        else:
            delta = value - self._previous_horizontal_scrollBar_value2
            self._previous_horizontal_scrollBar_value2 = value  # Update the previous value
            if delta > 0:
                # Scroll to the right
                self.sv2.horizontal_shift(1)
            elif delta < 0:
                # Scroll to the left
                self.sv2.horizontal_shift(-1)

    def link_vertical_scrollBar_with_Graph2(self, value):
        if value == 0:
            self.sv2.home_view()
        else:
            delta = value - self._previous_vertical_scrollBar_value2
            self._previous_vertical_scrollBar_value2 = value  # Update the previous value
            if delta > 0:
                # Scroll to the right
                self.sv2.vertical_shift(1)
            elif delta < 0:
                # Scroll to the left
                self.sv2.vertical_shift(-1)

    def toggle_play_pause_icon2(self):
        if self._play_pause_state2:
            self.sv2.play()
            self.play_pause_btn2.setIcon(QIcon('icons/pause.svg'))
            self._play_pause_state2 = False
        else:
            self.sv2.pause()
            self.play_pause_btn2.setIcon(QIcon('icons/play.svg'))
            self._play_pause_state2 = True

    def toggle_play_pause_icon3(self):
        if self._play_pause_state3:
            self.sv.play()
            self.sv2.play()
            self.play_pause_btn3.setIcon(QIcon('icons/pause.svg'))
            self._play_pause_state3 = False
        else:
            self.sv.pause()
            self.sv2.pause()
            self.play_pause_btn3.setIcon(QIcon('icons/play.svg'))
            self._play_pause_state3 = True



    def openCSV1(self, plot_widget):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open CSV', '', 'CSV Files (*.csv)', options=options)
        self.sv.load_dataset(file_name, 3)

        for i in range(len(self.sv.signals)):
            list_item = QListWidgetItem(f"{i} - Signal B")
            list_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)
            list_item.setCheckState(Qt.Checked)
            self.list_widget1.addItem(list_item)

    def openCSV2(self, plot_widget):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open CSV', '', 'CSV Files (*.csv)', options=options)
        self.sv2.load_dataset(file_name, 3)

        for i in range(len(self.sv2.signals)):
            list_item = QListWidgetItem(f"{i} - Signal B")
            list_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)
            list_item.setCheckState(Qt.Checked)
            self.list_widget2.addItem(list_item)


    # def list_signals_to_plot1(self):
    #     checked_signals_indices = []
    #     for i in range(self.list_widget1.count()):
    #         item = self.list_widget1.item(i)
    #         if item.checkState() == Qt.Checked:
    #             checked_signals_indices.append(self.sv.signals[self.list_widget1.row(item)])
    #     return checked_signals_indices

    def list_signals_to_plot1(self):
        checked_signals_indices = []
        for i in range(self.list_widget1.count()):
            item = self.list_widget1.item(i)
            if item.checkState() == Qt.Checked:
                checked_signals_indices.append(self.list_widget1.row(item))
        return checked_signals_indices
    def list_signals_to_plot2(self):
        checked_signals_indices = []
        for i in range(self.list_widget2.count()):
            item = self.list_widget2.item(i)
            if item.checkState() == Qt.Checked:
                checked_signals_indices.append(self.list_widget2.row(item))
        return checked_signals_indices

    # def add_signal_to_graph1(self):
    #     checked_signals_indices = self.list_signals_to_plot1()
    #     for signal in checked_signals_indices:
    #         if signal in self.sv.plotted_signals:
    #             checked_signals_indices.remove(signal)
    #
    #     for signal in checked_signals_indices:
    #         self.sv.add_signal(i, f"Signal A {i}", (int(random.random()*255), int(random.random()*255), int(random.random()*255)))
    #
    #     self._play_pause_state1 = False
    #     self.play_pause_btn1.setIcon(QIcon('icons/pause.svg'))

    def add_signal_to_graph1(self):
        checked_signals_indices = self.list_signals_to_plot1()
        for i in checked_signals_indices:
            if self.sv.signals[i] not in self.sv.plotted_signals:
                self.sv.add_signal(i, f"Signal A {i}", (int(random.random()*255), int(random.random()*255), int(random.random()*255)))
        self._play_pause_state1 = False
        self.play_pause_btn1.setIcon(QIcon('icons/pause.svg'))

    def add_signal_to_graph2(self):
        checked_signals_indices = self.list_signals_to_plot2()
        for i in checked_signals_indices:
            if self.sv2.signals[i] not in self.sv2.plotted_signals:
                self.sv2.add_signal(i, f"Signal B {i}", (int(random.random()*255), int(random.random()*255), int(random.random()*255)))
        self._play_pause_state2 = False
        self.play_pause_btn2.setIcon(QIcon('icons/pause.svg'))

    def replay_active_signal1(self):
        self.sv.replay()
        self.play_pause_btn1.setIcon(QIcon('icons/pause.svg'))
        self._play_pause_state1 = False
        self.sv.home_view()

    def replay_active_signal2(self):
        self.sv2.replay()
        self.play_pause_btn2.setIcon(QIcon('icons/pause.svg'))
        self._play_pause_state2 = False
        self.sv2.home_view()

    def replay_active_synchronous_signals(self):
        self.sv.replay()
        self.sv.home_view()
        self.sv2.replay()
        self.sv2.home_view()
        self.play_pause_btn3.setIcon(QIcon('icons/pause.svg'))
        self._play_pause_state3 = False


    def stop_active_signal1(self):
        self.sv.replay()
        self.play_pause_btn1.setIcon(QIcon('icons/play.svg'))
        self._play_pause_state1 = True
        self.sv.pause()
        self.sv.home_view()
    def stop_active_signal2(self):
        self.sv2.replay()
        self.play_pause_btn2.setIcon(QIcon('icons/play.svg'))
        self._play_pause_state2 = True
        self.sv2.pause()
        self.sv2.home_view()

    def stop_active_synchronous_signals(self):
        self.stop_active_signal1()
        self.stop_active_signal2()

    def reset_view1(self):
        self.sv.home_view()

    def reset_view2(self):
        self.sv2.home_view()

    def reset_synchronous_views(self):
        self.reset_view1()
        self.reset_view2()

    def remove_active_signal1(self):
        if self._signal1_is_hide:
            self.add_signal_to_graph1()
            self.play_pause_btn1.setIcon(QIcon('icons/play.svg'))
            self._play_pause_state1 = True
            self.hide_btn1.setIcon(QIcon('icons/eye.svg'))
            self._signal1_is_hide = False
        else:
            self.sv.remove()
            self.sv.pause()
            self.hide_btn1.setIcon(QIcon('icons/eye-crossed.svg'))
            self._signal1_is_hide = True
            self.play_pause_btn1.setIcon(QIcon('icons/play.svg'))
            self._play_pause_state1 = True


    def remove_active_signal2(self):
        self.sv2.remove()
        self.sv2.pause()
        self.play_pause_btn2.setIcon(QIcon('icons/play.svg'))
        self._play_pause_state2 = True

    def remove_active_synchronous_signals(self):
        self.remove_active_signal1()
        self.remove_active_signal2()

    def move_active_signal1_to_graph2(self):
        self.sv.moveTo(self.sv2)


    def move_active_signal2_to_graph1(self):
        self.sv2.moveTo(self.sv)

    def change_speed(self, graph, new_speed):
        if new_speed:
            graph.rate = new_speed

    def change_color(self, signals_list, new_color):
        for signal in signals_list:
            signal.color = self.color_dict[new_color]
            pen = pg.mkPen(signal.color, width=3)
            signal.plot_data_item.setPen(pen)


    def toggle_show_hide_signal(self, signal):
        pass

    def restart(self, graph):
        pass


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(Path('qss/lightStyle.qss').read_text())
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
