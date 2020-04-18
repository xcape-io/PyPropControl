#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
main.py

Educational example of Qt console props.

usage: python3 alphabet.py [-h] [-s SERVER] [-p PORT] [-d] [-l LOGGER]

optional arguments:
  -h, --help            show this help message and exit
  -s SERVER, --server SERVER
                        change MQTT server host
  -p PORT, --port PORT  change MQTT server port
  -d, --debug           set DEBUG log level
  -l LOGGER, --logger LOGGER
                        use logging config file

To switch MQTT broker, kill the program and start again with new arguments.
'''

import paho.mqtt.client as mqtt
import os, sys, platform, signal, uuid

os.chdir(os.path.dirname(os.path.abspath(__file__)))

from constants import *

try:
    PYPROPS_CORELIBPATH
    sys.path.append(PYPROPS_CORELIBPATH)
except NameError:
    pass

from CountdownApp import CountdownApp
from Singleton import Singleton, SingletonException

me = None
try:
	me = Singleton()
except SingletonException:
	sys.exit(-1)
except BaseException as e:
	print(e)

if USE_GPIO and os.path.isfile('/opt/vc/include/bcm_host.h'):
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

mqtt_client = mqtt.Client(uuid.uuid4().urn, clean_session=True, userdata=None)

app = CountdownApp(sys.argv, mqtt_client, debugging_mqtt=False)

# Assign handler for process exit (shows not effect on Windows in debug here)
signal.signal(signal.SIGTERM, app.quit)
signal.signal(signal.SIGINT, app.quit)
if platform.system() != 'Windows':
	signal.signal(signal.SIGHUP, app.quit)
	signal.signal(signal.SIGQUIT, app.quit)

app.start()

rc = app.exec_()

if USE_GPIO and os.path.isfile('/opt/vc/include/bcm_host.h'):
    GPIO.cleanup()

try:
	mqtt_client.disconnect()
	mqtt_client.loop_stop()
except:
	pass

del(me)

sys.exit(rc)
