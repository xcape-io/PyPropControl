#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LedWidget.py
MIT License (c) Marie Faure <dev at faure dot systems>

LED with status widget.
"""

from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QSizePolicy, QStackedWidget
from PyQt5.QtGui import QGuiApplication, QIcon, QPalette
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot

LED_COLOR_STYLE_RED = "red"


class LedWidget(QWidget):
    switched = pyqtSignal(str, str)

    # __________________________________________________________________
    def __init__(self, status, size):
        super(LedWidget, self).__init__()

        self._redAsBold = False
        self._redAsRed = False

        self._defaultText = status
        self._defaultTextColor = "#{0:02x}{1:02x}{2:02x}".format(QGuiApplication.palette().color(QPalette.Text).red(),
                                                                 QGuiApplication.palette().color(QPalette.Text).green(),
                                                                 QGuiApplication.palette().color(QPalette.Text).blue())

        self._ledImage = QStackedWidget()
        self._ledImage.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self._led = {}
        for color in ['black', 'blue', 'gray', 'green', 'orange', 'purple', 'red', 'yellow']:
            self._led[color] = QLabel()
            self._led[color].setPixmap(QIcon("./leds/led-{0}.svg".format(color)).pixmap(size))
            self._led[color].setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            self._ledImage.addWidget(self._led[color])

        self._ledStatus = QLabel(self._defaultText)
        self._ledStatus.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self._color = None

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(8)
        main_layout.addWidget(self._ledImage)
        main_layout.addWidget(self._ledStatus)

        self.setLayout(main_layout)

        self.switchOn('gray')

    # __________________________________________________________________
    def close(self):
        self._file.close()

    # __________________________________________________________________
    def color(self):
        return self._color

    # __________________________________________________________________
    def setRedAsBold(self, yes):
        self._redAsBold = yes

    # __________________________________________________________________
    def setRedAsRed(self, yes):
        self._redAsRed = yes

    @pyqtSlot(str, str)
    # __________________________________________________________________
    def switchOn(self, color, text=""):

        if not text:
            text = self._defaultText
        style_color = self._defaultTextColor
        style_weight = "normal"

        if color == 'red' and self._redAsBold:
            style_weight = "bold"

        if color == 'red' and self._redAsRed:
            style_color = LED_COLOR_STYLE_RED

        for c in ['black', 'blue', 'gray', 'green', 'orange', 'purple', 'red', 'yellow']:
            if color == c:
                self._ledImage.setCurrentWidget(self._led[color])
                self._color = color

        self._ledStatus.setStyleSheet("color: {0}; font-weight: {1}".format(style_color, style_weight))
        self._ledStatus.setText(text)

        self.switched.emit(color, text)
