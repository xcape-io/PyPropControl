#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SwitchWidget.py
MIT License (c) Faure Systems <dev at faure dot systems>

Prop switch widget.
"""

from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot, QSize
from PyQt5.QtGui import QIcon

import os


class SwitchWidget(QWidget):
    publishMessage = pyqtSignal(str, str)

    # __________________________________________________________________
    def __init__(self,
                 label,
                 variable,
                 image_on,
                 image_off,
                 sync,
                 sync_on, 
                 sync_off,
                 action_on,
                 action_off,
                 topic,
                 value_on='1',
                 value_off='0',
                 label_width=0):

        super(SwitchWidget, self).__init__()

        self._variable = variable
        self._value_on = value_on
        self._value_off = value_off
        self._image_on = QIcon(image_on)
        self._image_off = QIcon(image_off)
        self._sync = sync
        self._sync_on = sync_on
        self._sync_off = sync_off
        self._action_on = action_on
        self._action_off = action_off
        self._topic = topic

        self._dataLabel = QLabel(label + ' : ')
        self._dataLabel.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self._dataLabel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        if label_width:
            self._dataLabel.setFixedWidth(label_width)

        self._dataImage = QLabel()
        self._dataImage.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        self._dataImage.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self._buttonImage = QLabel()
        self._buttonImage.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self._buttonImage.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self._buttonImage.setMouseTracking(True)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(8)
        main_layout.addWidget(self._dataLabel)
        main_layout.addWidget(self._dataImage)
        main_layout.addWidget(self._buttonImage)

        self.setLayout(main_layout)

        self._button_on = QIcon(os.path.dirname(os.path.abspath(__file__)) + '/images/switch-on.svg')
        self._button_off = QIcon(os.path.dirname(os.path.abspath(__file__)) + '/images/switch-off.svg')

        self._dataImage.setPixmap(self._image_off.pixmap(QSize(20, 20)))
        self._buttonImage.setPixmap(self._button_off.pixmap(QSize(32, 18)))
        self._buttontoggled = False

    # __________________________________________________________________
    def mousePressEvent(self, event):

        self._buttontoggled = not self._buttontoggled

        if self._buttontoggled:
            self.publishMessage.emit(self._topic, self._action_on)
        else:
            self.publishMessage.emit(self._topic, self._action_off)

    # __________________________________________________________________
    @pyqtSlot(dict)
    def onDataReceived(self, variables):

        if self._variable in variables:
            if variables[self._variable] == self._value_on:
                self._dataImage.setPixmap(self._image_on.pixmap(QSize(20, 20)))
            else:
                self._dataImage.setPixmap(self._image_off.pixmap(QSize(20, 20)))

        if self._sync in variables:
            if variables[self._sync] == self._sync_on:
                self._buttonImage.setPixmap(self._button_on.pixmap(QSize(32, 18)))
                self._buttontoggled = True
            else:
                self._buttonImage.setPixmap(self._button_off.pixmap(QSize(32, 18)))
                self._buttontoggled = False
