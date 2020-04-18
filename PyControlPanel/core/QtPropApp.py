#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QtPropApp.py
MIT License (c) Marie Faure <dev at faure dot systems>

Props base class extends QtMqttApp:
- add automation
- agnostic to asyncio, Qt, Tkinter or Kivy
- add methods to support Room protocol like ArduinoProps
    DATA -> send variables to control
    MESG -> send text to display in control
    DONE -> acknowledge that a command has been performed
    OMIT -> acknowledge that a command has been ignored
    OVER -> notify that a challenge is over
    REQU -> request a command to another prop
    PROG -> request a control program
"""

from constants import *
from QtMqttApp import QtMqttApp

from PyQt5.QtCore import pyqtSlot, QTimer


class QtPropApp(QtMqttApp):

    # __________________________________________________________________
    def __init__(self, argv, client, debugging_mqtt=False):
        super().__init__(argv, client, debugging_mqtt)

        self._periodicActions = {}
        self._periodicTimers = []

        self.addPeriodicAction("send all data", self.sendAllData, PUBLISHALLDATA_PERIOD)

        QTimer.singleShot(0, self._startPeriodicTasks)

    # __________________________________________________________________
    @pyqtSlot()
    def _startPeriodicTasks(self):
        # Periodic actions
        for title, (func, time) in self._periodicActions.items():
            try:
                timer = QTimer()
                self._periodicTimers.append(timer) # to keep a reference
                timer.setInterval(time * 1000)
                timer.timeout.connect(func)
                QTimer.singleShot(0, timer.start)
                self._logger.info("Periodic task created '{0}' every {1} seconds".format(title, time))
            except Exception as e:
                self._logger.error("Failed to create periodic task '{0}'".format(title))
                self._logger.debug(e)

    # __________________________________________________________________
    def addData(self, data):
        self._publishable.append(data)

    # __________________________________________________________________
    def addPeriodicAction(self, title, func, time):
        if title in self._periodicActions:
            self._logger.warning("Duplicate periodic action ignored '{0}' every {1} seconds".format(title, time))
        else:
            self._periodicActions[title] = (func, time)
            self._logger.info("New periodic action added '{0}' every {1} seconds".format(title, time))

    # __________________________________________________________________
    @pyqtSlot()
    def sendAllData(self):
        self._publishAllData()

    # __________________________________________________________________
    @pyqtSlot()
    def sendDataChanges(self):
        self._publishDataChanges()

    # __________________________________________________________________
    @pyqtSlot(str)
    def sendData(self, data):
        self._publishMessage(self._mqttOutbox, "DATA " + data)

    # __________________________________________________________________
    @pyqtSlot(str)
    def sendDone(self, action):
        self._publishMessage(self._mqttOutbox, "DONE " + action)

    # __________________________________________________________________
    @pyqtSlot(str, str)
    def sendMesg(self, message, topic = None):
        if topic is None:
            self._publishMessage(self._mqttOutbox, "MESG " + message)
        else:
            self._publishMessage(topic, "MESG " + message)

    # __________________________________________________________________
    @pyqtSlot(str)
    def sendOmit(self, action):
        self._publishMessage(self._mqttOutbox, "OMIT " + action)

    # __________________________________________________________________
    @pyqtSlot(str)
    def sendOver(self, challenge):
        self._publishMessage(self._mqttOutbox, "OVER " + challenge)

    # __________________________________________________________________
    @pyqtSlot(str)
    def sendProg(self, program):
        self._publishMessage(self._mqttOutbox, "PROG " + program)

    # __________________________________________________________________
    @pyqtSlot(str, str)
    def sendRequ(self, request, topic = None):
        if topic is None:
            self._publishMessage(self._mqttOutbox, "REQU " + request)
        else:
            self._publishMessage(topic, "REQU " + message)
