#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MqttApplet.py
MIT License (c) Faure Systems <dev at faure dot systems>

Base class for xcape.io Room applet (PyQt5 console application with MQTT).
"""

from constants import *
try:
    APPLICATION
except NameError:
    APPLICATION = "Props"
try:
    CONFIG_FILE
except NameError:
    CONFIG_FILE = ".config.yml"
try:
    MQTT_DEFAULT_HOST
except NameError:
    MQTT_DEFAULT_HOST = "localhost"
try:
    MQTT_DEFAULT_PORT
except NameError:
    MQTT_DEFAULT_PORT = 1883
try:
    MQTT_DEFAULT_QoS
except NameError:
    MQTT_DEFAULT_QoS = 1
try:
    MQTT_KEEPALIVE
except NameError:
    MQTT_KEEPALIVE = 15

import argparse
import codecs
import configparser
import logging
import logging.config
import os
import yaml

from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication


class MqttApplet(QApplication):
    connectedToMqttBroker = pyqtSignal()
    disconnectedToMqttBroker = pyqtSignal()
    messageReceived = pyqtSignal(str, str)
    publishMessage = pyqtSignal(str, str)

    # __________________________________________________________________
    def __init__(self, argv, client, debugging_mqtt=False):

        super().__init__(argv)

        self.setApplicationName(APPLICATION)
        self.setOrganizationDomain(ORGANIZATIONDOMAIN)
        self.setOrganizationName(ORGANIZATIONNAME)

        self.publishMessage.connect(self._onPublishMessage)

        self._config = {}
        self._definitions = {}
        self._mqttSubscriptions = []
        self._mqttServerHost = MQTT_DEFAULT_HOST
        self._mqttServerPort = MQTT_DEFAULT_PORT
        self._publishable = []

        ini = 'definitions.ini'
        if os.path.isfile(ini):
            self._config = configparser.ConfigParser()
            self._config.read_file(codecs.open(ini, 'r', 'utf8'))
            if "mqtt" in self._config.sections():
                for key in self._config.options("mqtt"):
                    self._definitions[key] = self._config.get("mqtt", key)
                    if key.startswith('mqtt-sub-'):
                        self._mqttSubscriptions.append(self._definitions[key])

        if os.path.isfile(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as conffile:
                self._config = yaml.load(conffile, Loader=yaml.SafeLoader)
        else:
            self._config = {}

        print('Config:', self._config)

        self._mqttClient = client
        self._mqttConnected = False
        if 'host' in self._config:
            self._mqttServerHost = self._config['host']
        if 'port' in self._config:
            self._mqttServerPort = self._config['port']

        self._mqttClient.on_connect = self._mqttOnConnect
        self._mqttClient.on_disconnect = self._mqttOnDisconnect
        self._mqttClient.on_message = self._mqttOnMessage
        self._mqttClient.on_publish = self._mqttOnPublish
        self._mqttClient.on_subscribe = self._mqttOnSubscribe
        self._mqttClient.on_unsubscribe = self._mqttOnUnsubscribe

        if debugging_mqtt:
            self._mqttClient.on_log = self._mqttOnLog

        parser = argparse.ArgumentParser()
        parser.add_argument("-s", "--server", help="change MQTT server host", nargs=1)
        parser.add_argument("-p", "--port", help="change MQTT server port", nargs=1, type=int)
        parser.add_argument("-d", "--debug", help="set DEBUG log level", action='store_true')
        parser.add_argument("-l", "--logger", help="use logging config file", nargs=1)

        try:
            args = vars(parser.parse_args())

            if args['server']:
                self._mqttServerHost = args['server'][0]
                self._config['host'] = self._mqttServerHost

            if args['port']:
                self._mqttServerPort = args['port'][0]
                self._config['port'] = self._mqttServerHost

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
                ch = logging.FileHandler('prop.log', 'w')
                ch.setLevel(logging.INFO)
                self._logger.addHandler(ch)

            with open(CONFIG_FILE, 'w') as conffile:
                yaml.dump(self._config, conffile, default_flow_style=False)
        except:
            pass

    # __________________________________________________________________
    def isConnectedToMqttBroker(self):

        return self._mqttConnected

    # __________________________________________________________________
    def _mqttOnConnect(self, client, userdata, flags, rc):

        if rc == 0:
            self._mqttConnected = True
            # self._logger.debug("Connected to MQTT server with flags: ", flags) # flags is dict
            self._logger.info(self.tr("Program connected to MQTT server"))
            self.connectedToMqttBroker.emit()
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
    def _mqttOnDisconnect(self, client, userdata, rc):

        self._mqttConnected = False
        self._logger.info(self.tr("Program disconnected from MQTT server"))
        self.disconnectedToMqttBroker.emit()

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
    def _mqttOnLog(self, client, userdata, level, buf):

        self._logger.debug("Paho log level {0} : {1}".format(level, buf))

    # __________________________________________________________________
    def _mqttOnMessage(self, client, userdata, msg):

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
    def _mqttOnPublish(self, client, userdata, mid):

        self._logger.debug("MQTT message is published : mid=%s userdata=%s", mid, userdata)
        self._logger.info("{0} (mid={1})".format(self.tr("Message published"), mid))

    # __________________________________________________________________
    def _mqttOnSubscribe(self, client, userdata, mid, granted_qos):

        self._logger.debug("MQTT topic is subscribed : mid=%s granted_qos=%s", mid, granted_qos)  # granted_qos is (2,)
        self._logger.info(
            "{0} (mid={1}) {2} {3}".format(self.tr("Program susbcribed to topic"), mid, self.tr("with QoS"),
                                           granted_qos))  # mid is a number (count)

    # __________________________________________________________________
    def _mqttOnUnsubscribe(self, client, userdata, mid):

        self._logger.debug("MQTT topic is unsubscribed : mid=%s", mid)
        self._logger.info("{0} (mid={1})".format(self.tr("Program has been unsusbcribed from topic"), mid))


    # __________________________________________________________________
    @pyqtSlot(str, str)
    def _onPublishMessage(self, topic, message):

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

    # __________________________________________________________________
    @logger.setter
    def logger(self, value):
        self._logger = value
