#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AppletDialog.py
MIT License (c) Faure Systems <dev at faure dot systems>

Main dialog of an applet.
"""

from constants import *
try:
    LAYOUT_FILE
except NameError:
    LAYOUT_FILE = ".layout.yml"

from PyQt5.QtCore import pyqtSignal, pyqtSlot, QPoint, QSize, QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QDialog
import os, yaml


class AppletDialog(QDialog):

    # __________________________________________________________________
    def __init__(self, title, icon, logger):

        super().__init__()

        self._logger = logger

        self._logger.info(self.tr("GUI started"))

        QApplication.desktop().screenCountChanged.connect(self.restoreWindow)
        QApplication.desktop().resized.connect(self.restoreWindow)

        self.setWindowTitle(title)
        self.setWindowIcon(QIcon(icon))

        self._buildUi()

        QTimer.singleShot(0, self.layoutLoadSettings);

    # __________________________________________________________________
    def _buildUi(self):

        pass

    # __________________________________________________________________
    def closeEvent(self, event):

        self._logger.info(self.tr("Done with GUI"))

    # __________________________________________________________________
    @pyqtSlot()
    def layoutLoadSettings(self):

        layout = {}
        layout['x'] = 200
        layout['y'] = 200
        layout['w'] = 400
        layout['h'] = 400

        layout['position'] = QPoint(200, 200)
        layout['size'] = QSize(400, 400)

        if os.path.isfile(LAYOUT_FILE):
            with open(LAYOUT_FILE, 'r') as layoutfile:
                layout = yaml.load(layoutfile, Loader=yaml.SafeLoader)

        self.move(QPoint(layout['x'], layout['y']))
        self.resize(QSize(layout['w'], layout['h']))

    # __________________________________________________________________
    @pyqtSlot()
    def layoutSaveSettings(self):

        layout = {}
        layout['x'] = self.pos().x()
        layout['y'] = self.pos().y()
        layout['w'] = self.size().width()
        layout['h'] = self.size().height()

        with open(LAYOUT_FILE, 'w') as layoutfile:
            yaml.dump(layout, layoutfile, default_flow_style=False)

    # __________________________________________________________________
    def moveEvent(self, event):

        if self.isVisible():
            QTimer.singleShot(0, self.layoutSaveSettings);

    # __________________________________________________________________
    @pyqtSlot()
    def restoreWindow(self):

        self.resize(QSize(400, 400))
        self.move(QPoint(200, 200))

    # __________________________________________________________________
    def resizeEvent(self, event):

        if self.isVisible():
            QTimer.singleShot(0, self.layoutSaveSettings);
