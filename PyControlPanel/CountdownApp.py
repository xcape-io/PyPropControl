#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
CountdownApp.py

CountdownApp application extends SketchApp.

Sainsmart Relay 16: inpu are active LOW (apply 0 to switch ON)

'''

import os, sys

from PyQt5.QtMultimedia import QSound
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot

from PropData import PropData
from QtPropApp import QtPropApp
from CountdownWidget import CountdownWidget

from constants import *

if USE_GPIO and os.path.isfile('/opt/vc/include/bcm_host.h'):
    import RPi.GPIO as GPIO


class CountdownApp(QtPropApp):
    chronoUpdated = pyqtSignal(str, bool)

    # __________________________________________________________________
    def __init__(self, argv, client, debugging_mqtt=False):

        super().__init__(argv, client, debugging_mqtt)

        self._seconds = 0
        self._overtime = False

        self._chrono_p = PropData('chrono', str, '00:00', logger=self._logger)
        self.addData(self._chrono_p)

        self._overtime_p = PropData('overtime', bool, 0, alias=("yes", "no"), logger=self._logger)
        self.addData(self._overtime_p)

        style = ""
        qss = open("Countdown.css",'r')
        with qss:
            style = style + qss.read()

        self._mainWidget = CountdownWidget(self._logger)
        self._mainWidget.setStyleSheet(style)
        self._mainWidget.aboutToClose.connect(self.exitOnClose)
        self._mainWidget.show()

        self._mainWidget.showFullScreen()
        self._mainWidget.setCursor(Qt.BlankCursor)
        self.chronoUpdated.connect(self._mainWidget.setTime)

    # __________________________________________________________________
    @pyqtSlot()
    def exitOnClose(self):
        self._logger.info(self.tr("exitOnClose "))
        self.quit()

    # __________________________________________________________________
    def onConnect(self, client, userdata, flags, rc):
        # extend as a virtual method
        self.sendAllData()

    # __________________________________________________________________
    def onMessage(self, topic, message):
        #print(topic, message)
        #self.processEvents()
        if topic == self._mqttInbox:
            if message == "app:startup":
                self.sendAllData()
                self.sendDone(message)
            elif message == "app:data":
                self.sendAllData()
                self.sendDone(message)
        elif topic == self._definitions['mqtt-sub-countdown-seconds']:
            try:
                self._seconds = int(message)
                if self._seconds < 0:
                    self._overtime_p.update(True)
                    seconds = -self._seconds
                else:
                    self._overtime_p.update(False)
                    seconds = self._seconds
                mm = int(seconds / 60)
                ss = seconds - mm * 60
                self._chrono_p.update("{:0>2d}:{:0>2d}".format(mm, ss))
                #self._mainWidget.setTime(self._chrono_p.value(), self._overtime_p.value())
                self.chronoUpdated.emit(self._chrono_p.value(), self._overtime_p.value())
                self.sendDataChanges()
            except Exception as e:
                if self._logger:
                    self._logger.error("Failed to parse seconds : " + message)
                    self._logger.debug(e)
        else:
            self.sendOmit(message)
