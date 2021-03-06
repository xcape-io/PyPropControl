﻿# PyRoomPlugin
*<a href="https://www.learnpyqt.com/" target="_blank">PyQt5</a> applet to quickly create a plugin for <a href="https://xcape.io/" target="_blank">xcape.io</a> Room.*

In the area of ​​Escape Room creation, we need to code quickly and reliably, and we need to streamline and reuse our code.

From this plugin skeleton you can write a plugin for *<a href="https://xcape.io/" target="_blank">xcape.io</a> __Room__* software in minutes.

![](screenshots/shot.png)
 
To write your very first **Room** plugin, we recommend you follow the 
<a href="https://xcape.io/public/documentation/en/room/Plugintutorial.html" target="_blank">Plugin tutorial</a> in the <a href="https://xcape.io/public/documentation/en/room/Help.html" target="_blank">**Room** manual</a>.
 
## Installation

1. First install Python 3.8.x in `C:\Python38` ([Windows x86-64 executable installer](https://www.python.org/ftp/python/3.8.2/python-3.8.2-amd64.exe) from <a href="https://www.python.org/downloads/release/python-382/" target="_blank">python.org</a>)

2. Download [`PyRoomPluginInstallation.zip`](https://github.com/xcape-io/PyPropControl/raw/master/PyRoomPlugin/PyRoomPluginInstallation.zip) from this GitHub repository 

3. Unflate it in your plugin folder

4. Run `install.bat` with a double-click to create the Python virtual environment (*venv*).

5. Set MQTT broker IP address in `constants.py`

    ```python
    MQTT_DEFAULT_HOST = 'localhost'  # replace localhost with your broker IP address
    ```

6. Run `test.bat` to test your new panel.

You are now ready to hack a new plugin :
* add it to ***Room*** software (<a href="https://xcape.io/public/documentation/en/room/AddEchoPlugintoyourroom.html" target="_blank">see ***Room*** manual</a>)
* create a new PyCharm project in the plugin folder (<a href="https://xcape.io/public/documentation/en/room/EditEchopluginwithPyCharm.html" target="_blank">see ***Room*** manual</a>)


## Creating your own Room plugin
<a href="https://www.jetbrains.com/pycharm/download/" target="_blank">Pycharm Community</a> is the free python IDE recommenbded for developing your own plugin.

1. Edit `definitions.ini` to set the MQTT topics for your prop

2. Edit `constants.py` to set your prop name and other constants specific to your plugin

3. Edit `PluginDialog.py` to develop your own plugin

In `./core` folder you will find the most useful widgets for building a plugin:

* **<a href="https://github.com/xcape-io/PyPropControl/blob/master/core/AppletDialog.py" target="_blank">`AppletDialog`</a>**: base class that manages the size and position of the main dialog
* **<a href="https://github.com/xcape-io/PyPropControl/blob/master/core/MqttApplet.py" target="_blank">`MqttApplet`</a>**: base class for you applet which manage all the MQTT messaging
* **<a href="https://github.com/xcape-io/PyPropControl/blob/master/core/Singleton.py" target="_blank">`Singleton`</a>**: to guarantee the execution of a single instance of your applet
* **<a href="https://github.com/xcape-io/PyPropControl/blob/master/core/LedWidget.py" target="_blank">`LedWidget`</a>**: to show the conenction state with the prop
* **<a href="https://github.com/xcape-io/PyPropControl/blob/master/core/DataWidget.py" target="_blank">`DataWidget`</a>**: display a prop data with text or image
* **<a href="https://github.com/xcape-io/PyPropControl/blob/master/core/PushButton.py" target="_blank">`PushButton`</a>**: button to send a message to the prop
* **<a href="https://github.com/xcape-io/PyPropControl/blob/master/core/SwitchWidget.py" target="_blank">`SwitchWidget`</a>**: switch synchronized with a prop boolean data
* **<a href="https://github.com/xcape-io/PyPropControl/blob/master/core/ToggleButton.py" target="_blank">`ToggleButton`</a>**: toggle button synchronized with a prop boolean data


## Author

**Faure Systems** (Apr 19th, 2020)
* company: FAURE SYSTEMS SAS
* mail: *dev at faure dot systems*
* github: <a href="https://github.com/fauresystems?tab=repositories" target="_blank">fauresystems</a>
* web: <a href="https://faure.systems/" target="_blank">Faure Systems</a>