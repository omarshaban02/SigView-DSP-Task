PATH = 'signals/mitbih_train.csv'

import numbers
import signal
from turtle import title, width
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
import pandas as pd
import pyqtgraph as pg
import random


class Signal(object):
    def __init__(self, data: list = [], title: str = '', color: tuple = (0, 0, 0)) -> None:
        self.completed = False
        self.plotted_data = []
        self.data = data
        self.stop_drawing = False
        self.current_sample_index = 0
        self.current_sample = 0
        self.is_active = False
        self.plot_data_item = pg.PlotDataItem()
        self._color = color
        self._title = None
        self._on_click_event_handler = lambda e: None
        self.plot_data_item.setCurveClickable(state=True, width=6)

    @property
    def on_click_event_handler(self):
        return self._on_click_event_handler

    @on_click_event_handler.setter
    def on_click_event_handler(self, func):
        self._on_click_event_handler = func
        self.plot_data_item.sigClicked.connect(self._on_click_event_handler)

    @property
    def title(self):
        return self._title

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value
        pen = pg.mkPen(self.color, width=1)
        self.plot_data_item.setPen(pen)

    @title.setter
    def title(self, value: pg.TextItem):
        self._title = value

    def setTitleColor(self, color: tuple) -> None:
        self.title.setColor(color)

    # update current sample, plot data and current sample index.
    def advance(self):
        if not (self.stop_drawing or self.completed):
            self.current_sample = self.data[self.current_sample_index]
            self.plotted_data.append(self.current_sample)
            self.current_sample_index += 1
            if len(self.data) == len(self.plotted_data):
                self.completed = True
                self.stop_drawing = True

    def pause(self) -> None:
        self.stop_drawing = True

    def resume(self) -> None:
        self.stop_drawing = False

    def plot(self) -> None:
        self.plot_data_item.clear()
        self.plot_data_item.setData(self.plotted_data)

    def restart(self) -> None:
        self.plotted_data = []
        self.completed = False
        self.stop_drawing = False
        self.current_sample = 0
        self.current_sample_index = 0


class SignalViewerLogic(object):
    def __init__(self, view: pg.PlotWidget) -> None:

        self.view = view
        self.timer = QTimer()
        self.timer.timeout.connect(self.draw)
        self.signals: list(Signal) = []  # storing loaded signals from the file
        self.plotted_signals: list(Signal) = []  # storing all signals in the view
        self._active_signals: list(Signal) = []  # storing the active signals e.g. clicked signals
        self._rate = 20  # samples per second
        self.timer.start(int(1000 / self._rate))
        self.view_width = 50
        self.view_height = 1
        self._xRange = [0, self.view_width]
        self._yRange = [0, self.view_height]
        self._display_axis = True
        self._display_grid = False
        self.view.setXRange(self._xRange[0], self._xRange[1], padding=0)
        self.view.setYRange(self._yRange[0], self._yRange[1], padding=0)
        self.view.scene().sigMouseClicked.connect(self.ignore_focus)

    def ignore_focus(self, e):
        if e.double():
            for signal in self.plotted_signals:
                signal.is_active = False
                pen = pg.mkPen(signal.color, width=1)
                signal.plot_data_item.setPen(pen)

    @property
    def display_axis(self):
        return self._display_axis

    @display_axis.setter
    def display_axis(self, value):
        self.display_axis = value
        # do something

    @property
    def display_grid(self):
        return self._display_grid

    @display_grid.setter
    def display_grid(self, value):
        self._display_grid = value
        # do something

    @property
    def rate(self):
        return self._rate

    @rate.setter
    def rate(self, value):
        self.timer.stop()
        self._rate = value
        duration = 1000 / self._rate
        self.timer.start(int(duration))

    @property
    def active_signals(self):
        self._active_signals = []
        for signal in self.plotted_signals:
            if signal.is_active:
                self._active_signals.append(signal)
        return self._active_signals

    @property
    def yRange(self) -> list:
        return self.view.viewRange()[1]

    @yRange.setter
    def yRange(self, value: list):
        self.view.setYRange(value[0], value[1], padding=0)
        self._yRange = self.view.viewRange()[1]

    @property
    def xRange(self) -> list:
        return self.view.viewRange()[0]

    @xRange.setter
    def xRange(self, value: list):

        self.view.setXRange(value[0], value[1], padding=0)
        self._xRange = self.view.viewRange()[0]

    def set_title(self, title: str):
        self.view.setTitle(title)

    def load_dataset(self, filename: str, loaded_signals: int = None) -> None:
        signals = []
        if loaded_signals is None:
            signals = pd.read_csv(filename).to_numpy()
        else:
            signals = pd.read_csv(filename).head(loaded_signals).to_numpy()

        for s in signals:
            sig = Signal(data=s)
            self.signals.append(sig)

    def zoom_in(self, scale: int) -> None:
        self.view.scaleBy(s=(scale, scale))

    def zoom_out(self, scale: int) -> None:
        f = 1 / scale
        self.view.scaleBy(s=(f, f))

    def activate_signal(self, index: int) -> None:
        signal = self.signals[index]
        signal.is_active = True
        pen = pg.mkPen(signal.color, width=3)
        signal.plot_data_item.setPen(pen)

    def zoom(self, scale: int) -> None:
        v = self.view.getViewBox()
        v.scaleBy(s=(scale, scale))
        self.view.plotItem.scaleBy(s=(scale, scale))

    # the default direction is along positive y-axis as step is positive integer
    def vertical_shift(self, step: int) -> None:
        self.yRange = [self.yRange[0] + step, self.yRange[1] + step]

    # the default direction is along positive x-axis as step is positive integer
    def horizontal_shift(self, step: int) -> None:
        self.xRange = [self.xRange[0] + step, self.xRange[1] + step]

    # go to the home view
    def home_view(self) -> None:
        self.xRange = [0, self.view_width]
        self.yRange = [0, self.view_height]

    # apply the action on the active signals
    def play(self):
        signals = self.active_signals
        for signal in signals:
            signal.resume()

    # apply the action on the active signals
    def pause(self):
        signals = self.active_signals
        for signal in signals:
            signal.pause()

    # apply the action on the active signals
    def replay(self):
        signals = self.active_signals
        for signal in signals:
            signal.restart()

    # apply the action on the active signals
    def set_signal_title(self, signal: Signal, text: str, color=(255, 255, 255)):
        pos_x = 0
        pos_y = -len(self.plotted_signals)
        title = pg.TextItem(text=text, color=color, anchor=(pos_x, pos_y))
        signal.title = title

    # apply the action on the active signals
    def export(self):
        pass

    # apply the action on the active signals
    # draw active signals
    # this method is called by the rate specified above, default is 20 times per second
    def draw(self):
        for signal in self.plotted_signals:
            if not (signal.stop_drawing or signal.completed):
                if signal.current_sample_index > self.xRange[1]:
                    self.horizontal_shift(1)
                signal.advance()
                signal.plot()

    def signal_onclick(self, e):
        signal = None
        for s in self.plotted_signals:
            if id(e) == id(s.plot_data_item):
                signal = s

        signal.is_active = True
        pen = pg.mkPen(signal.color, width=3)
        e.setPen(pen)

    # add signal to the plotted signal and active signals and start drawing it
    def add_signal(self, index: int, name: str, color=(255, 255, 255)):
        signal = self.signals[index]
        signal.is_active = True
        signal.color = color
        signal.on_click_event_handler = lambda e: self.signal_onclick(e)
        self.set_signal_title(signal, name)
        self.plotted_signals.append(signal)
        self.view.addItem(signal.title)
        self.view.addItem(signal.plot_data_item)

    # apply the action on the active signals
    # clear the active signals
    def remove(self):
        for signal in self.active_signals:
            self.view.removeItem(signal.plot_data_item)
            self.view.removeItem(signal.title)
            self.plotted_signals.remove(signal)

    # clear the screen
    def clear(self):
        self.plotted_signals = []
