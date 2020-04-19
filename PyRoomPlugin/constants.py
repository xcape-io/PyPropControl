#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
constants.py

Contains all the Room Control applet constants.
"""

# __________________________________________________________________
# Required by MqttApplet
ORGANIZATIONDOMAIN = "xcape.io"
ORGANIZATIONNAME = "xcape.io"

CONFIG_FILE = '.config.yml'

APPLICATION = "Room"

PYPROPS_CORELIBPATH = '../core'

MQTT_DEFAULT_HOST = 'localhost'
MQTT_DEFAULT_PORT = 1883
MQTT_DEFAULT_QoS = 1

# __________________________________________________________________
# Required by PluginApplet
APPDISPLAYNAME = "Room"  # the Room Control application

# __________________________________________________________________
# Required by the widgets
LAYOUT_FILE = '.layout.yml'

# __________________________________________________________________
# Required by the application
PROP_NAME = 'Arduino Blink'
