#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
main.py
MIT License (c) Marie Faure <dev at faure dot systems>

Room (xcape.io) plugin.

usage: python main.py [-h] [-s SERVER] [-p PORT] [-d] [-l LOGGER]

optional arguments:
  -h, --help            show this help message and exit
  -s SERVER, --server SERVER
                        change MQTT server host
  -p PORT, --port PORT  change MQTT server port
  -d, --debug           set DEBUG log level
  -l LOGGER, --logger LOGGER
                        use logging config file

To switch MQTT broker, kill the program and start again with new arguments.
"""

from PyQt5.QtCore import QUuid
from PyQt5.QtGui import QIcon

import paho.mqtt.client as mqtt
import os,  sys,  platform, signal

from PluginApplet import PluginApplet
from Singleton import Singleton, SingletonException


me = None
try:
	me = Singleton()
except SingletonException:
	sys.exit(-1)
except BaseException as e:
	print(e)
	
os.chdir(os.path.dirname(os.path.abspath(__file__)))

clientid = "Xcape/Plugin/" + QUuid.createUuid().toString()

mqtt_client = mqtt.Client(clientid, clean_session=True, userdata=None)

applet = PluginApplet(sys.argv,  mqtt_client,  debugging_mqtt=True)

applet.setApplicationDisplayName("Room")
applet.setWindowIcon(QIcon('./room.png'));

if applet.logger:
	applet.logger.info(applet.tr("Session started"))

# Assign handler for process exit (shows not effect on Windows in debug here)
signal.signal(signal.SIGTERM, applet.quit)
signal.signal(signal.SIGINT, applet.quit)
if platform.system() != 'Windows':
	signal.signal(signal.SIGHUP, applet.quit)
	signal.signal(signal.SIGQUIT, applet.quit)

applet.start()

rc = applet.exec_()

try:
	mqtt_client.disconnect()
	mqtt_client.loop_stop()
except:
	pass
	
if applet.logger:
	applet._logger.info(applet.tr("Session done"))

del me

sys.exit(rc)
