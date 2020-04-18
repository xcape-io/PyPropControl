#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AppletDialog.py
MIT License (c) Marie Faure <dev at faure dot systems>

Main dialog of an applet.
"""

from PyQt5.QtCore import pyqtSignal, pyqtSlot, QSettings, QPoint, QSize, QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QDialog


class AppletDialog(QDialog):
    switchLed = pyqtSignal(str, str)

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
    def layoutLoadSettings(self):

        settings = QSettings("settings.ini", QSettings.IniFormat);
        settings.setIniCodec("UTF-8");

        settings.beginGroup("Layout")
        pos = settings.value("position", QPoint(200, 200))
        size = settings.value("size", QSize(400, 400))
        settings.endGroup()

        self.move(pos)
        self.resize(size)

    # __________________________________________________________________
    def layoutSaveSettings(self):

        settings = QSettings("settings.ini", QSettings.IniFormat);
        settings.setIniCodec("UTF-8");
        settings.beginGroup("Layout")
        settings.setValue("position", self.pos())
        settings.setValue("size", self.size())
        settings.endGroup()
        settings.sync()

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
