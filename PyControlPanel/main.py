#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
main.py
MIT License (c) Faure Systems <dev at faure dot systems>

MQTT control panel.

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
import paho.mqtt.client as mqtt
import os, sys, platform, signal, uuid

os.chdir(os.path.dirname(os.path.abspath(__file__)))

from constants import *

if os.path.exists('./core'):
	sys.path.append('./core')
else:
	try:
		PYPROPS_CORELIBPATH
		sys.path.append(PYPROPS_CORELIBPATH)
	except NameError:
		pass

from PyQt5.QtGui import QIcon

from PanelApplet import PanelApplet
from Singleton import Singleton, SingletonException


me = None
try:
	me = Singleton()
except SingletonException:
	sys.exit(-1)
except BaseException as e:
	print(e)

mqtt_client = mqtt.Client(uuid.uuid4().urn, clean_session=True, userdata=None)

applet = PanelApplet(sys.argv,  mqtt_client,  debugging_mqtt=True)

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
