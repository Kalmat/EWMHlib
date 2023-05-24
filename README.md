# EWMH-lib
[![Type Checking](https://github.com/Kalmat/EWMHlib/actions/workflows/type-checking.yml/badge.svg)](https://github.com/Kalmat/EWMHlib/actions/workflows/type-checking.yml)[![PyPi version](https://pypip.in/v/$REPO/badge.png)](https://crate.io/packages/$REPO/)

Extended Window Manager Hints implementation in Python 3 which allows to easily query and control 
Window Managers which follow these standards.

It also adds some additional, useful features like catching and handling events.

For more information, refer to official documentation at: https://specifications.freedesktop.org/wm-spec/latest/

**Warning: new Display Server used by GNOME in Ubuntu, Wayland, is not EWMH-compliant, so some features will not work**


### RootWindow: Root queries, changes and messages

Base class to access root features.

If you need to address default root window, you can simply use `defaultRootWindow` object, which will give you
instant access to all root-related features (it is equivalent to: `myRoot = RootWindow()`)

To get a RootWindow object it is necessary to pass the target root id. This can be achieved in several ways:

- You already have a root, so pass root.id param
- You have some criteria to select a root, so use the convenience function `getAllDisplaysInfo()`, to look for all roots and select the desired one
- You have a target window, so use the convenience function getDisplayFromWindow(window.id), so you will retrieve the associated display connection and root window
- Instantiate this class with no param (None), so it will retrieve the default display and root

Apart from given methods, you can access these other values to be used with python-xlib:

- display: XDisplay connection
- screen: screen Struct
- root: root X Window object
- id: root window id


#### WM Protocols

WM_PROTOCOLS messages (PING/SYNC) are accessible using wmProtocols subclass (RootWindow.wmProtocols.Ping/Sync)


### EwmhWindow: Window queries, changes and messages

Base class to access application windows related features.

To instantiate this class only a window id is required. It is possible to retrieve this value in several ways:

- Target a specific window using an external module (e.g. `PyWinCtl.getAllWindowsWithTitle(title)`)
- Retrieve it from your own application (e.g. PyQt's `winId()` or TKinter's `frame()`)

Note that, although a root is also a window, these methods will not likely work with it.

Apart from given methods, there are some values you can use with python-xlib:

- display: XDisplay connection
- root: root X Window object
- rootWindow: object to access RootWindow methods
- xWindow: X Window object associated to current window
- id: current window's id

Additional, non-EWMH features, related to low-level window properties like hints, protocols and events are
available using extensions subclass (EwmhWindow.extensions.*), see below.


#### Extensions: Hints, Protocols and Events

Additional, non-EWMH features, related to low-level window properties like hints, protocols and events.


### General variables

As their names suggest, these general variables will give access to the default display, screen
and root objects, allowing to perform all Xlib-related functions.

|    Objects     |
|:--------------:|
| defaultDisplay |
| defaultScreen  |
|  defaultRoot   |


### Display functions

These functions will allow to manage/find proper display, in a multi-display environment
(not the usual scenario, so the objects above will be enough in most cases).
 

|  Display functions   |
|:--------------------:|
|    getAllDisplays    |
|  getDisplayFromRoot  |
| getDisplayFromWindow |


### Properties and Messages functions  

This set of functions will allow to directly query and control application or root windows, without the
need of instantiation their corresponding classes described above. These are very similar to
their Xlib equivalent functions (more complex to use), but they add some useful help in order to handle 
values, atoms and so on.

|  Property functions  |
|:--------------------:|
|     getProperty      |
|   getPropertyValue   |
|    changeProperty    |
|     sendMessage      |


### Properties, atoms and hints values

These values are accessible through `Props` class (ewmhlib.Props.*). 
They include all properties, atoms and hints values recognized by EWMH specs, so makes it easier 
to know, enumerate or use them.

They have been organized in different subclasses, according to their type or when they should be used.

### Data Structs

Aimed to facilitate understanding and handling complex reply data structures and fields.

| Data Structs  |
|:-------------:|
| DisplaysInfo  |
|  ScreensInfo  |
|    WmHints    |
| WmNormalHints |


## INSTALL <a name="install"></a>

To install this module on your system, you can use pip: 

    pip3 install ewmhlib

or

    python3 -m pip install ewmhlib

Alternatively, you can download the wheel file (.whl) available in the [Download page](https://pypi.org/project/EWMHlib/#files) and the [dist folder](https://github.com/Kalmat/EWMHlib/tree/master/dist), and run this (don't forget to replace 'x.x.xx' with proper version number):

    pip install EWMHlib-x.x.xx-py3-none-any.whl

You may want to add `--force-reinstall` option to be sure you are installing the right dependencies version.

Then, you can use it on your own projects just importing it:

    import ewmhlib

## SUPPORT <a name="support"></a>

In case you have a problem, comments or suggestions, do not hesitate to [open issues](https://github.com/Kalmat/EWMHlib/issues) on the [project homepage](https://github.com/Kalmat/EWMHlib)

## USING THIS CODE <a name="using"></a>

If you want to use this code or contribute, you can either:

* Create a fork of the [repository](https://github.com/Kalmat/EWMHlib), or 
* [Download the repository](https://github.com/Kalmat/EWMHlib/archive/refs/heads/master.zip), uncompress, and open it on your IDE of choice (e.g. PyCharm)

Be sure you install all dependencies described on "docs/requirements.txt" by using pip

## TEST <a name="test"></a>

To test this module on your own system, cd to "tests" folder and run:

    python3 test_ewmhlib.py
 