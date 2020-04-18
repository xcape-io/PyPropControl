#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CountdownFrame.py
MIT License (c) Marie Faure <dev at faure dot systems>

Countdown main widget.
"""

from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QLabel


class CountdownWidget(QWidget):
    aboutToClose = pyqtSignal()

    # __________________________________________________________________
    def __init__(self, logger):
        super().__init__()

        self._logger = logger

        # always on top sometimes doesn't work
        #self.setAttribute(Qt.WA_AlwaysStackOnTop)
        # frame only if not in fullscreen
        #self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint)

        self._buildUi()

    # __________________________________________________________________
    def _buildUi(self):

        main_layout = QVBoxLayout()
        chrono_layout = QHBoxLayout()

        self._chronoLabel = QLabel("00:00")
        self._chronoLabel.setObjectName('chrono')
        self._chronoLabel.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        chrono_layout.addStretch()
        chrono_layout.addWidget(self._chronoLabel)
        chrono_layout.addStretch()

        main_layout.addStretch()
        main_layout.addLayout(chrono_layout)
        main_layout.addStretch()

        self.setLayout(main_layout)

    # __________________________________________________________________
    def closeEvent(self, e):
        self.aboutToClose.emit()

    # __________________________________________________________________
    @pyqtSlot(str, bool)
    def setTime(self, timestr, overtime):
        # we could use a pyqtSlot here
        if overtime:
            self._chronoLabel.setStyleSheet("color: red")
        else:
            self._chronoLabel.setStyleSheet("color: white")
        self._chronoLabel.setText(timestr)

