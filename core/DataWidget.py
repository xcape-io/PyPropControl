#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DataWidget.py
MIT License (c) Faure Systems <dev at faure dot systems>

Prop data widget.
"""

from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt, pyqtSlot, QSize
from PyQt5.QtGui import QIcon

class DataWidget(QWidget):

    # __________________________________________________________________
    def __init__(self, label, variable, value_on='1', value_off='0', image_on=None, image_off=None, label_width=0):
        super(DataWidget, self).__init__()

        self._variable = variable
        self._value_on = value_on
        self._value_off = value_off
        if image_on is not None and image_off is not None:
            self._image_on = QIcon(image_on)
            self._image_off = QIcon(image_off)
            self._image = True
        else:
            self._image_on = None
            self._image_off = None
            self._image = False

        self._dataLabel = QLabel(label + ' : ')
        self._dataLabel.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self._dataLabel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        if label_width:
            self._dataLabel.setFixedWidth(label_width)

        self._dataValue = QLabel()
        self._dataValue.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(8)
        main_layout.addWidget(self._dataLabel)
        main_layout.addWidget(self._dataValue)

        self.setLayout(main_layout)

        if self._image:
            self._dataValue.setPixmap(self._image_off.pixmap(QSize(20, 20)))

    # __________________________________________________________________
    @pyqtSlot(dict)
    def onDataReceived(self, variables):

        if self._variable in variables:
            if self._image:
                if variables[self._variable] == self._value_on:
                    self._dataValue.setPixmap(self._image_on.pixmap(QSize(20, 20)))
                else:
                    self._dataValue.setPixmap(self._image_off.pixmap(QSize(20, 20)))
            else:
                self._dataValue.setText(variables[self._variable])
