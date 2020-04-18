#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MqttApplet.py
MIT License (c) Marie Faure <dev at faure dot systems>

Base class for xcape.io Room applet (PyQt5 console application with MQTT).
"""

from constants import *
import logging, logging.config
import argparse, os
from PyQt5.QtCore import QSettings, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication

MQTT_KEEPALIVE = 15  # 15 seconds is default MQTT_KEEPALIVE in Arduino PubSubClient.h


class MqttApplet(QApplication):
    messageReceived = pyqtSignal(str, str)
    publishMessageRequest = pyqtSignal(str, str)

    # __________________________________________________________________
    def __init__(self, argv, client, debugging_mqtt=False):

        super().__init__(argv)

        self.setApplicationName(APPNAME)

        settings = QSettings("settings.ini", QSettings.IniFormat);
        settings.setIniCodec("UTF-8");
        settings.beginGroup("MQTT")

        self.publishMessageRequest.connect(self.publishMessage)

        self._definitions = {}
        self._mqttSubscriptions = []

        if os.path.isfile('definitions.ini'):
            definitions = QSettings('definitions.ini', QSettings.IniFormat)
            for group in definitions.childGroups():
                definitions.beginGroup(group)
                if group == "mqtt":
                    for key in definitions.childKeys():
                        self._definitions[key] = definitions.value(key)
                        if key.startswith('mqtt-sub-'):
                            self._mqttSubscriptions.append(self._definitions[key])
                definitions.endGroup()

        self._mqttClient = client
        self._mqttConnected = False

        self._mqttServerHost = settings.value('host', MQTT_DEFAULT_HOST)
        self._mqttServerPort = settings.value('port', MQTT_DEFAULT_PORT, type=int)

        self._mqttClient.on_connect = self.mqttOnConnect
        self._mqttClient.on_disconnect = self.mqttOnDisconnect
        self._mqttClient.on_message = self.mqttOnMessage
        self._mqttClient.on_publish = self.mqttOnPublish
        self._mqttClient.on_subscribe = self.mqttOnSubscribe
        self._mqttClient.on_unsubscribe = self.mqttOnUnsubscribe

        if debugging_mqtt:
            self._mqttClient.on_log = self.mqttOnLog

        parser = argparse.ArgumentParser()
        parser.add_argument("-s", "--server", help="change MQTT server host", nargs=1)
        parser.add_argument("-p", "--port", help="change MQTT server port", nargs=1, type=int)
        parser.add_argument("-d", "--debug", help="set DEBUG log level", action='store_true')
        parser.add_argument("-l", "--logger", help="use logging config file", nargs=1)

        try:
            args = vars(parser.parse_args())

            if args['server']:
                self._mqttServerHost = args['server'][0]
                settings.setValue('host', self._mqttServerHost)

            if args['port']:
                self._mqttServerPort = args['port'][0]
                settings.setValue('port', self._mqttServerPort)

            if args['logger'] and os.path.isfile(args['logger']):
                logging.config.fileConfig(args['logger'])
                if args['debug']:
                    self._logger = logging.getLogger('debug')
                    self._logger.setLevel(logging.DEBUG)
                else:
                    self._logger = logging.getLogger('production')
                    self._logger.setLevel(logging.INFO)
            elif os.path.isfile('logging.ini'):
                logging.config.fileConfig('logging.ini')
                if args['debug']:
                    self._logger = logging.getLogger('debug')
                    self._logger.setLevel(logging.DEBUG)
                else:
                    self._logger = logging.getLogger('production')
                    self._logger.setLevel(logging.INFO)
            else:
                if args['debug']:
                    self._logger = logging.getLogger('debug')
                    self._logger.setLevel(logging.DEBUG)
                else:
                    self._logger = logging.getLogger('production')
                    self._logger.setLevel(logging.INFO)
                ch = logging.FileHandler('plugin.log', 'w')
                ch.setLevel(logging.INFO)
                self._logger.addHandler(ch)
        except:
            pass

    # __________________________________________________________________
    def isConnectedToMqttBroker(self):

        return self._mqttConnected

    # __________________________________________________________________
    def mqttOnConnect(self, client, userdata, flags, rc):

        if rc == 0:
            self._mqttConnected = True
            # self._logger.debug("Connected to MQTT server with flags: ", flags) # flags is dict
            self._logger.info(self.tr("Program connected to MQTT server"))
            for topic in self._mqttSubscriptions:
                try:
                    (result, mid) = self._mqttClient.subscribe(topic, MQTT_DEFAULT_QoS)
                    self._logger.info("{0} (mid={1}) : {2}".format(self.tr("Program subscribing to topic"), mid, topic))
                except Exception as e:
                    self._logger.error(self.tr("MQTT API : failed to call subscribe()"))
                    self._logger.debug(e)
        elif rc == 1:
            self._logger.warning(
                self.tr("Program failed to connect to MQTT server :  connection refused - incorrect protocol version"))
        elif rc == 2:
            self._logger.warning(
                self.tr("Program failed to connect to MQTT server : connection refused - invalid client identifier"))
        elif rc == 3:
            self._logger.warning(
                self.tr("Program failed to connect to MQTT server : connection refused - server unavailable"))
        elif rc == 4:
            self._logger.warning(
                self.tr("Program failed to connect to MQTT server : connection refused - bad username or password"))
        elif rc == 5:
            self._logger.warning(
                self.tr("Program failed to connect to MQTT server : connection refused - not authorised"))
        else:
            self._logger.warning(
                "{0} {1}".format(self.tr("Program failed to connect to MQTT server : return code was"), rc))

    # __________________________________________________________________
    def mqttOnDisconnect(self, client, userdata, rc):

        self._mqttConnected = False
        self._logger.info(self.tr("Program disconnected from MQTT server"))

        serv = ''
        if isinstance(userdata, str):
            try:
                mydata = eval(userdata)
                if isinstance(mydata, dict) and 'host' in mydata and 'port' in mydata:
                    serv = mydata['host'] + ':' + str(mydata['port'])
            except Exception as e:
                self._logger.debug(self.tr("MQTT client userdata not as expected"))
                self._logger.debug(e)

        if serv:
            self._logger.warning(
                "{0}{1} {2} {3}".format(self.tr("Disconnected from MQTT server with rc="), rc, self.tr("from"), serv))
        else:
            self._logger.warning("{0}{1}".format(self.tr("Disconnected from MQTT server with rc="), rc))

    # __________________________________________________________________
    def mqttOnLog(self, client, userdata, level, buf):

        self._logger.debug("Paho log level {0} : {1}".format(level, buf))

    # __________________________________________________________________
    def mqttOnMessage(self, client, userdata, msg):

        message = None
        try:
            message = msg.payload.decode(encoding="utf-8", errors="strict")
        except:
            pass

        if message:
            self._logger.info(self.tr("Message received : '") + message + self.tr("' in ") + msg.topic)
            self.messageReceived.emit(msg.topic, message)
        else:
            self._logger.warning("{0} {1}".format(self.tr("MQTT message decoding failed on"), msg.topic))

    # __________________________________________________________________
    def mqttOnPublish(self, client, userdata, mid):

        self._logger.debug("MQTT message is published : mid=%s userdata=%s", mid, userdata)
        self._logger.info("{0} (mid={1})".format(self.tr("Message published"), mid))

    # __________________________________________________________________
    def mqttOnSubscribe(self, client, userdata, mid, granted_qos):

        self._logger.debug("MQTT topic is subscribed : mid=%s granted_qos=%s", mid, granted_qos)  # granted_qos is (2,)
        self._logger.info(
            "{0} (mid={1}) {2} {3}".format(self.tr("Program susbcribed to topic"), mid, self.tr("with QoS"),
                                           granted_qos))  # mid is a number (count)

    # __________________________________________________________________
    def mqttOnUnsubscribe(self, client, userdata, mid):

        self._logger.debug("MQTT topic is unsubscribed : mid=%s", mid)
        self._logger.info("{0} (mid={1})".format(self.tr("Program has been unsusbcribed from topic"), mid))

    # __________________________________________________________________
    @pyqtSlot(str, str)
    def publishMessage(self, topic, message):

        if self._mqttConnected:
            try:
                (result, mid) = self._mqttClient.publish(topic, message, qos=MQTT_DEFAULT_QoS, retain=False)
                self._logger.info(
                    "{0} '{1}' (mid={2}) on {3}".format(self.tr("Program sending message"), message, mid, topic))
            except Exception as e:
                self._logger.error(
                    "{0} '{1}' on {2}".format(self.tr("MQTT API : failed to call publish() for"), message, topic))
                self._logger.debug(e)
        else:
            self._logger.info("{0} : '{1}'".format(self.tr("Program failed to send message (disconnected)"), message))

    # __________________________________________________________________
    @pyqtSlot()
    def quit(self):

        QApplication.quit()

    # __________________________________________________________________
    def start(self):

        mydata = {'host': self._mqttServerHost, 'port': self._mqttServerPort}
        self._mqttClient.user_data_set(str(mydata))

        """
		The loop_start() starts a new thread, that calls the loop method at 
		regular intervals for you. It also handles re-connects automatically.
		"""
        self._mqttClient.loop_start()

        """
		If you use client.connect_async(), your client must use the 
		threaded interface client.loop_start()
		"""
        try:
            self._mqttClient.connect_async(self._mqttServerHost, port=self._mqttServerPort, keepalive=MQTT_KEEPALIVE)
            self._logger.info(
                self.tr("Program initiated asynchronous connection to ") + self._mqttServerHost + ":" + str(
                    self._mqttServerPort))
        except Exception as e:
            self._logger.error(self.tr("MQTT API : failed to call connect_async()"))
            self._logger.debug(e)

    # __________________________________________________________________
    @property
    def logger(self):
        return self._logger
