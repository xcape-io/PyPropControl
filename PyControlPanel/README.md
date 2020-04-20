
# PyControlPanel
*<a href="https://www.learnpyqt.com/" target="_blank">PyQt5</a> applet to create a prop control panel.*

In the area of ​​Escape Room creation, we need to code quickly and reliably, and we need to streamline and reuse our code.

From this control panel skeleton you can write a prop control panel in minutes.

![](screenshots/shot.png)
 
 
## Installation

1. First install Python 3.8.x in `C:\Python38` ([Windows x86-64 executable installer](https://www.python.org/ftp/python/3.8.2/python-3.8.2-amd64.exe) from <a href="https://www.python.org/downloads/release/python-382/" target="_blank">python.org</a>)

2. Download [`PanelInstallation.zip`](https://github.com/xcape-io/PyPropControl/raw/master/PyPropControlPanel/PanelInstallation.zip) from this GitHub repository 

3. Unflate it in your panel folder

4. Run `install.bat` with a double-click to create the Python virtual environment (*venv*).

5. Run `test.bat` to test your new panel.


## Creating your own control panel
<a href="https://www.jetbrains.com/pycharm/download/" target="_blank">Pycharm Community</a> is the free python IDE recommenbded for developing your own control panel.

1. Edit `definitions.ini` to set the MQTT topics for your prop

2. Edit `constants.py` to set your prop name and other constants specific to your application

3. Edit `PluginDialog.py` to develop your own prop control panel

In `./core` folder you will find the most useful widgets for building a control panel:

* <a href="https://github.com/xcape-io/PyPropControl/blob/master/core/DataWidget.py" target="_blank">DataWidget</a>
* PushButton
* SwitchWidget
* <a href="https://github.com/xcape-io/PyPropControl/blob/master/core/ToggleButton.py" target="_blank">ToggleButton</a>

## Author

**Marie FAURE** (Apr 19th, 2020)
* company: FAURE SYSTEMS SAS
* mail: *dev at faure dot systems*
* github: <a href="https://github.com/fauresystems?tab=repositories" target="_blank">fauresystems</a>
* web: <a href="https://faure.systems/" target="_blank">Faure Systems</a>