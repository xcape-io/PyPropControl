#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PushButton.py
MIT License (c) Marie Faure <dev at faure dot systems>

Prop control push buttob.
"""

from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout
from PyQt5.QtCore import pyqtSignal, pyqtSlot

class PushButton(QWidget):
    publishMessage = pyqtSignal(str, str)

    # __________________________________________________________________
    def __init__(self, caption, action, topic):
        super(PushButton, self).__init__()

        self._action = action
        self._topic = topic

        self._pushButton = QPushButton(caption)

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
