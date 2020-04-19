#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PluginApplet.py
MIT License (c) Marie Faure <dev at faure dot systems>

PluginApplet application extends MqttApplet.
"""

from constants import *
from MqttApplet import MqttApplet
from PluginDialog import PluginDialog
from PyQt5.QtCore import pyqtSignal, pyqtSlot


class PluginApplet(MqttApplet):
    propsMessageReceived = pyqtSignal(str)

    # __________________________________________________________________
    def __init__(self, argv, client, debugging_mqtt=False):
        super().__init__(argv, client, debugging_mqtt)

        self.setApplicationDisplayName(APPDISPLAYNAME)

        # on_message per topic callbacks
        try:
            mqtt_sub_props = self._definitions['mqtt-sub-prop']
            self._mqttClient.message_callback_add(mqtt_sub_props, self._mqttOnMessageFromProps)
        except Exception as e:
            self._logger.error(self.tr("Plugin sub topic definition is missing"))
            self._logger.debug(e)

        # on_message default callback
        self._mqttClient.on_message = self._mqttOnMessage

        self._PluginDialog = PluginDialog(self.tr("Plugin"), './room.png', self._logger)
        self._PluginDialog.aboutToClose.connect(self.exitOnClose)
        self.propsMessageReceived.connect(self._PluginDialog.onPropsMessage)
        self._PluginDialog.show()

    # __________________________________________________________________
    @pyqtSlot()
    def exitOnClose(self):
        self._logger.info(self.tr("exitOnClose "))
        self.quit()

    # __________________________________________________________________
    def _mqttOnMessage(self, client, userdata, msg):
        message = None
        try:
            message = msg.payload.decode(encoding="utf-8", errors="strict")
        except:
            pass

        if message:
            self._logger.info(self.tr("Message received : '") + message + self.tr("' in ") + msg.topic)
        ##self.messageReceived.emit(msg.topic, message)
        else:
            self._logger.warning("{0} {1}".format(self.tr("MQTT message decoding failed on"), msg.topic))

    # __________________________________________________________________
    def _mqttOnMessageFromProps(self, client, userdata, msg):
        message = None
        try:
            message = msg.payload.decode(encoding="utf-8", errors="strict")
        except:
            pass

        if message:
            self._logger.info(
                self.tr("Message received from Plugin props : '") + message + self.tr("' in ") + msg.topic)
            self.propsMessageReceived.emit(message)
        else:
            self._logger.warning(
                "{0} {1}".format(self.tr("Decoding MQTT message from Plugin props failed on"), msg.topic))
