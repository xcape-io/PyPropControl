#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PushButton.py
MIT License (c) Faure Systems <dev at faure dot systems>

Prop control push button.
"""

from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt

class PushButton(QWidget):
    publishMessage = pyqtSignal(str, str)

    # __________________________________________________________________
    def __init__(self, caption, action, topic):
        super(PushButton, self).__init__()

        self._action = action
        self._topic = topic

        self._pushButton = QPushButton(caption)
        self._pushButton.setFocusPolicy(Qt.NoFocus)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(8)
        main_layout.addWidget(self._pushButton)

        self.setLayout(main_layout)

        self._pushButton.released.connect(self.onPushButton)

    # __________________________________________________________________
    @pyqtSlot()
    def onPushButton(self):

        self.publishMessage.emit(self._topic, self._action)
