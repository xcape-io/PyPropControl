#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
constants.py

Contains all the Control Panel applet constants.
"""

# __________________________________________________________________
# Required by MqttApplet
ORGANIZATIONDOMAIN = "xcape.io"
ORGANIZATIONNAME = "xcape.io"

CONFIG_FILE = '.config.yml'

APPLICATION = "Control Panel"

PYPROPS_CORELIBPATH = '../core' # however ./core is preferred if present

MQTT_DEFAULT_HOST = 'localhost'
MQTT_DEFAULT_PORT = 1883
MQTT_DEFAULT_QoS = 1

# __________________________________________________________________
# Required by PanelApplet
APPDISPLAYNAME = APPLICATION

# __________________________________________________________________
# Required by the widgets
LAYOUT_FILE = '.layout.yml'
LABELS_WIDTH = 50

# __________________________________________________________________
# Required by the application
PROP_NAME = 'Arduino Blink'

DATALED_IMAGE_ON = './images/'
DATALED_IMAGE_OFF = ''
