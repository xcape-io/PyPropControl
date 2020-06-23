# PyQt5 Prop Control library
*<a href="https://www.learnpyqt.com/" target="_blank">PyQt5</a> library to create control panels for escape room props.*

The [PyPropControl core library](https://github.com/xcape-io/PyPropControl#pypropcontrol-core-library) is shared by two projects:
* [PyControlPanel](https://github.com/xcape-io/PyPropControl#pycontrolpanel)
* [PyRoomPlugin](https://github.com/xcape-io/PyPropControl#pyroomplugin)

[QtProp](https://github.com/xcape-io/PyProps/tree/master/QtProp) in [PyProps library](https://github.com/xcape-io/PyProps) is also written with <a href="https://www.learnpyqt.com/" target="_blank">PyQt5</a> therefore we, **and you**, can leverage in coding prop control panels and *<a href="https://xcape.io/" target="_blank">xcape.io Room</a>*.

<a href="https://www.learnpyqt.com/" target="_blank">PyQt5</a> has its own event loop to multitask seamlessly and it brings the power of <a href="https://doc.qt.io/" target="_blank">Qt</a> to Python.

<a href="https://www.jetbrains.com/pycharm/download/" target="_blank">Pycharm Community</a> is the free python IDE recommenbded for developing your own plugin or control panel.

The PyControlPanel code and the PyRoomPlugin code are almost interchangeable.

## PyControlPanel
See [PyControlPanel project](https://github.com/xcape-io/PyPropControl/tree/master/PyControlPanel#pycontrolpanel).

Prop control panel is a powerful feature of *<a href="https://xcape.io/" target="_blank">xcape.ioRoom</a>* software and for people who don't want to use *<a href="https://xcape.io/" target="_blank">xcape.io Room</a>*, **PyControlPanel** is the alternative to create your own prop control panel.

### Create your own prop control panel
The control panel code is mainly in `PanelDialog.py` where you start editing for your own project.

To create your own control panel, you simply download the [`PyPropControlPanelInstallation.zip`](https://github.com/xcape-io/PyPropControl/raw/master/PyControlPanel/PyControlPanelInstallation.zip) archive, unflate and hack the code.

Because *PyControlPanel* is a pure python applet, you can install it on any computer running python with <a href="https://www.learnpyqt.com/" target="_blank">PyQt5</a> (Windows, Mac, Linux and even Raspberry Pi).

See <a href="https://github.com/xcape-io/PyPropControl/tree/master/PyControlPanel#installation" target="_blank">Installation</a> in PyPropControlPanel README.

### Make a simple or a complex control panel
You can quickly write a control panel with the widgets from the core library:

* **<a href="https://github.com/xcape-io/PyPropControl/blob/master/core/DataWidget.py" target="_blank">DataWidget</a>**
* **<a href="https://github.com/xcape-io/PyPropControl/blob/master/core/LedWidget.py" target="_blank">LedWidget</a>**
* **<a href="https://github.com/xcape-io/PyPropControl/blob/master/core/PushButton.py" target="_blank">PushButton</a>**
* **<a href="https://github.com/xcape-io/PyPropControl/blob/master/core/SwitchWidget.py" target="_blank">SwitchWidget</a>**
* **<a href="https://github.com/xcape-io/PyPropControl/blob/master/core/ToggleButton.py" target="_blank">ToggleButton</a>**

And because you code the control panel yourself, you can create widgets of any kind to make a complex control panel.


## PyRoomPlugin
See [PyRoomPlugin project](https://github.com/xcape-io/PyPropControl/tree/master/PyRoomPlugin#pyroomplugin).

The *<a href="https://xcape.io/" target="_blank">xcape.ioRoom</a>* plugin system allows you to extend the software to meet all the needs of escape rooms.

Plugin are usually created to perform specific control, synch as:
* send clues and hint to players (<a href="https://github.com/xcape-io/PyTeletextPlugin" target="_blank">PyTeletextPlugin</a>)
* adjust the timing of a linear actuator
* control a game with several boards (biometric fingerprint in an out) 

The plugin code is mainly in `PluginDialog.py` where you start editing for your own project.

You will use the widgets of the [PyPropControl core library](https://github.com/xcape-io/PyPropControl#pypropcontrol-core-library) and you will create your own widgets easily thanks to the <a href="https://doc.qt.io/qt-5/qtwidgets-module.html" target="_blank">QtWidgets library</a> and the <a href="https://www.learnpyqt.com/" target="_blank">PyQt5 tutorials</a>.

## PyPropControl core library 
See <a href="https://github.com/xcape-io/PyPropControl/tree/master/core" target="_blank">PyPropControl core</a>.

* `AppletDialog`: base class that manages the size and position of the main dialog
* `MqttApplet`: base class for you applet which manage all the MQTT messaging
* `Singleton`: to guarantee the execution of a single instance of your applet
* `LedWidget`: to show teh conenction state with the prop
* `DataWidget`: display a prop data with text or image
* `PushButton`: button to send a message to the prop
* `SwitchWidget`: switch synchronized with a prop boolean data
* `ToggleButton`: toggle button synchronized with a prop boolean data

![Prop control panel](PyControlPanel/screenshots/shot.png)

## Author

**Faure Systems** (Apr 18th, 2020)
* company: FAURE SYSTEMS SAS
* mail: *dev at faure dot systems*
* github: <a href="https://github.com/xcape-io?tab=repositories" target="_blank">xcape-io</a>
* web: <a href="https://xcape.io/" target="_blank">xcape.io</a>