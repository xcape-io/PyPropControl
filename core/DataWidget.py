#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DataWidget.py
MIT License (c) Marie Faure <dev at faure dot systems>

Prop data widget.
"""

from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt, pyqtSlot


class DataWidget(QWidget):

    # __________________________________________________________________
    def __init__(self, label, variable):
        super(DataWidget, self).__init__()

        self._variable = variable

        self._dataLabel = QLabel(label + ' : ')
        self._dataLabel.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self._dataLabel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self._dataValue = QLabel()
        self._dataValue.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(8)
        main_layout.addWidget(self._dataLabel)
        main_layout.addWidget(self._dataValue)

        self.setLayout(main_layout)

    # __________________________________________________________________
    @pyqtSlot(dict)
    def onDataReceived(self, variables):

        if self._variable in variables:
            self._dataValue.setText(variables[self._variable])
