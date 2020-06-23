#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ToggleButton.py
MIT License (c) Faure Systems <dev at faure dot systems>

Prop control toggle button.
"""

from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt

class ToggleButton(QWidget):
    publishMessage = pyqtSignal(str, str)

    # __________________________________________________________________
    def __init__(self,
                 caption_on,
                 caption_off,
                 variable,
                 sync_on,
                 sync_off,
                 action_on,
                 action_off,
                 topic):

        super(ToggleButton, self).__init__()

        self._caption_on = caption_on
        self._caption_off = caption_off
        self._variable = variable
        self._sync_on = sync_on
        self._sync_off = sync_off
        self._action_on = action_on
        self._action_off = action_off
        self._topic = topic

        self._pushButton = QPushButton(self._caption_off)
        self._pushButton.setFocusPolicy(Qt.NoFocus)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(8)
        main_layout.addWidget(self._pushButton)

        self.setLayout(main_layout)

        self._pushButton.released.connect(self.onPushButton)

    # __________________________________________________________________
    @pyqtSlot(dict)
    def onDataReceived(self, variables):

        if self._variable in variables:
            if variables[self._variable] == self._sync_on:
                self._pushButton.setText(self._caption_on)
            else:
                self._pushButton.setText(self._caption_off)

    # __________________________________________________________________
    @pyqtSlot()
    def onPushButton(self):

        if self._pushButton.text() == self._caption_on:
            self.publishMessage.emit(self._topic, self._action_on)
        else:
            self.publishMessage.emit(self._topic, self._action_off)
