# EWMH-lib
[![Type Checking](https://github.com/Kalmat/EWMHlib/actions/workflows/type-checking.yml/badge.svg)](https://github.com/Kalmat/EWMHlib/actions/workflows/type-checking.yml)
[![PyPI version](https://badge.fury.io/py/ewmhlib.svg)](https://badge.fury.io/py/ewmhlib)
[![Documentation Status](https://readthedocs.org/projects/ewmhlib/badge/?version=latest)](https://ewmhlib.readthedocs.io/en/latest/?badge=latest)


Extended Window Manager Hints implementation in Python 3 and python-xlib, which allows to easily query and control 
Window Managers following these standards.

It also adds some additional, useful features like managing hints and handling events.

For more information, refer to official documentation at: https://specifications.freedesktop.org/wm-spec/latest/

This module has been tested OK in Ubuntu/GNOME, Mint/Cinnamon and Manjaro/KDE. If you have issues in other EWMH-compliant environments, do not hesitate to [open an issue](https://github.com/Kalmat/EWMHlib/issues) in the [project homepage](https://github.com/Kalmat/EWMHlib)

**Warning: new Display Server used by GNOME in Ubuntu, Wayland, is not EWMH-compliant, so many features will not work**

## General functions and variables

These functions and variables are module-level, so they do not need to previously instantiate any class or object.

### General objects

As their names suggest, these general variables will give access to the default display, screen
and root objects, allowing to use them in Xlib-related functions.

|                    Objects                    |
|:---------------------------------------------:|
|                defaultDisplay                 |
|                 defaultScreen                 |
|                  defaultRoot                  |


### General functions

These functions will allow to manage/find displays, screens and roots, in a multi-display or multi-screen environment
(not the usual scenario, so the default objects above will be enough in most cases).
 
|                     Display functions                      |
|:----------------------------------------------------------:|
|      [getDisplaysInfo](docstrings.md#getdisplaysinfo)      |
|   [getDisplayFromRoot](docstrings.md#getdisplayfromroot)   |
| [getDisplayFromWindow](docstrings.md#getdisplayfromwindow) |
|             [getRoots](docstrings.md#getroots)             |

## EwmhRoot: Root queries, changes and messages

Class to access root features.

If you need to address default root window, you can simply use `defaultRootWindow` object, which will give you
instant access to all root-related features (it is equivalent to: `myRoot = EwmhRoot()`)

To get a EwmhRoot object it is necessary to pass the target root id. This can be achieved in several ways:

- You already have a root, so pass root.id param
- You have some criteria to select a root, so use the convenience function `getDisplaysInfo()`, to look for all roots and select the desired one
- You have a target window, so use the convenience function `getDisplayFromWindow(window.id)`, so you will retrieve the associated display connection and root window
- Instantiate this class with no param (None), so it will retrieve the default display and root

Note that, even though a regular (application) window has the same type than a root window, 
these methods will not work with it, so avoid passing it to instantiate this class.
 
|                       EwmhRoot methods                       |
|:------------------------------------------------------------:|
|     [getSupportedHints](docstrings.md#getsupportedhints)     |
|         [getClientList](docstrings.md#getclientlist)         |
| [getClientListStacking](docstrings.md#getclientliststacking) |
|   [getNumberOfDesktops](docstrings.md#getnumberofdesktops)   |
|   [setNumberOfDesktops](docstrings.md#setnumberofdesktops)   |
|    [getDesktopGeometry](docstrings.md#getdesktopgeometry)    |
|    [setDesktopGeometry](docstrings.md#setdesktopgeometry)    |
|    [getDesktopViewport](docstrings.md#getdesktopviewport)    |
|    [setDesktopViewport](docstrings.md#setdesktopviewport)    |
|     [getCurrentDesktop](docstrings.md#getcurrentdesktop)     |
|     [setCurrentDesktop](docstrings.md#setcurrentdesktop)     |
|       [getDesktopNames](docstrings.md#getdesktopnames)       |
|       [getActiveWindow](docstrings.md#getactivewindow)       |
|           [getWorkArea](docstrings.md#getworkarea)           |
|  [getSupportingWMCheck](docstrings.md#getsupportingwmcheck)  |
|       [getVirtualRoots](docstrings.md#getvirtualroots)       |
|      [setDesktopLayout](docstrings.md#setdesktoplayout)      |
|     [getShowingDesktop](docstrings.md#getshowingdesktop)     |
|     [setShowingDesktop](docstrings.md#setshowingdesktop)     |
|             [setClosed](docstrings.md#setclosed)             |
|         [setMoveResize](docstrings.md#setmoveresize)         |
|       [setWmMoveResize](docstrings.md#setwmmoveresize)       |
|         [setWmStacking](docstrings.md#setwmstacking)         |
|   [requestFrameExtents](docstrings.md#requestframeextents)   |


WM_PROTOCOLS messages are accessible using wmProtocols subclass (EwmhRoot.wmProtocols.Ping/Sync)
 
| EwmhRoot WMProtocols methods |
|:----------------------------:|
|  [ping](docstrings.md#ping)  |
|  [sync](docstrings.md#sync)  |


Apart from given methods, you can access these other variables (EwmhRoot.*) to be used with python-xlib. In most 
cases these values will match default general variables described above.

- display: XDisplay connection the root belongs to
- screen: screen Struct the root belongs to
- root: root as X Window object
- id: root window id

## EwmhWindow: Window queries, changes and messages

Class to access application window features.

To instantiate this class only a window id is required. It is possible to retrieve this value in several ways:

- Target a specific window using an external module (e.g. `pywinctl.getAllWindowsWithTitle(title)` or `pywinctl.getActiveWindow()`)
- Retrieve it from your own application (e.g. PyQt's `winId()` or TKinter's `frame()`)

Note that, although a root is also a window, most of these methods will not likely work with it.
 
|                     EwmhRoot methods                     |
|:--------------------------------------------------------:|
|             [getName](docstrings.md#getname)             |
|             [setName](docstrings.md#setname)             |
|      [getVisibleName](docstrings.md#getvisiblename)      |
|      [setVisibleName](docstrings.md#setvisiblename)      |
|         [getIconName](docstrings.md#geticonname)         |
|         [setIconName](docstrings.md#seticonname)         |
|  [getVisibleIconName](docstrings.md#getvisibleiconname)  |
|  [setVisibleIconName](docstrings.md#setvisibleiconname)  |
|          [getDesktop](docstrings.md#getdesktop)          |
|          [setDesktop](docstrings.md#setdesktop)          |
|     [getWmWindowType](docstrings.md#getwmwindowtype)     |
|     [setWmWindowType](docstrings.md#setwmwindowtype)     |
|          [getWmState](docstrings.md#getwmstate)          |
|       [changeWmState](docstrings.md#changewmstate)       |
|        [setMaximized](docstrings.md#setmaximized)        |
|        [setMinimized](docstrings.md#setminimized)        |
|   [getAllowedActions](docstrings.md#getallowedactions)   |
|            [getStrut](docstrings.md#getstrut)            |
|            [setStrut](docstrings.md#setstrut)            |
|     [getStrutPartial](docstrings.md#getstrutpartial)     |
|     [getIconGeometry](docstrings.md#geticongeometry)     |
|              [getPid](docstrings.md#getPid)              |
|     [getHandledIcons](docstrings.md#gethandledicons)     |
|         [getUserTime](docstrings.md#getUserTime)         |
|     [getFrameExtents](docstrings.md#getframeextents)     |
|     [getOpaqueRegion](docstrings.md#getopaqueregion)     |
| [getBypassCompositor](docstrings.md#getbypasscompositor) |
|           [setActive](docstrings.md#setactive)           |
|           [setClosed](docstrings.md#setclosed)           |
|      [changeStacking](docstrings.md#changestacking)      |
|       [setMoveResize](docstrings.md#setmoveresize)       |
|     [setMoveWmResize](docstrings.md#setwmmoveresize)     |
|       [setWmStacking](docstrings.md#setwmstacking)       |
| [requestFrameExtents](docstrings.md#requestframeextents) |


Apart from given methods, there are some values you can use with python-xlib:

- display: XDisplay connection the window belongs to
- screen: screen Struct the window belongs to
- root: root the window belongs to as X Window object
- rootWindow: object to access EwmhRoot methods corresponding to the root to which the window belongs
- xWindow: X Window object associated to current window
- id: current window id

Additional, non-EWMH features, related to low-level window properties like hints, protocols and events are
available using extensions subclass (EwmhWindow.extensions.*), see below.

### EwmhWindow Extensions: Geometry, Hints, Protocols and Events

Additional, non-EWMH features, related to low-level window properties like geometry, hints, protocols and events. 
They can be accessed using EwmhWindow.Extensions.*

|                 Extensions methods                 |
|:--------------------------------------------------:|
|       [getWmHints](docstrings.md#getwmhints)       |
|       [setWmHints](docstrings.md#setwmhints)       |
| [getWmNormalHints](docstrings.md#getwmnormalhints) |
| [setWmNormalHints](docstrings.md#setwmnormalhints) |
|   [getWmProtocols](docstrings.md#getwmprotocols)   |
|   [addWmProtocols](docstrings.md#addwmprotocols)   |
|   [delWmProtocols](docstrings.md#delwmprotocols)   |
|      [CheckEvents](docstrings.md#checkevents)      |


| Extensions.CheckEvents Methods |
|:------------------------------:|
|  [start](docstrings.md#start)  |
|  [pause](docstrings.md#pause)  |
|   [stop](docstrings.md#stop)   |


Events loop example:

    import time
    
    import Xlib.protocol
    import Xlib.X
    
    from ewmhlib import EwmhRoot, EwmhWindow
    
    root = EwmhRoot()
    w = root.getActiveWindow()
    if w:
        win = EwmhWindow(w)

    def callback(event: Xlib.protocol.rq.Event):
        print("EVENT RECEIVED", event)

    win.extensions.checkEvents.start([Xlib.X.ConfigureNotify, Xlib.X.ConfigureRequest, Xlib.X.ClientMessage],
                                     Xlib.X.StructureNotifyMask | Xlib.X.SubstructureNotifyMask,
                                     callback)

    print("MANUALLY MOVE AND RESIZE ACTIVE WINDOW")
    print("Press Ctl-C to exit")
    while True:
        try:
            time.sleep(0.1)
        except KeyboardInterrupt:
            break
    win.extensions.checkEvents.stop()


## Properties and Messages functions  

This set of functions will allow to directly query and control application or root windows, without the
need of instantiating their corresponding classes described above. 

These are very similar to their Xlib equivalent functions (more complex to use than the methods provided by 
EwmhRoot and EwmhWindow classes), and therefore will allow custom, more advanced, perhaps more specific and/or non 
fully EWMH standard features; but they add some useful help in order to simplify handling replies, values, atoms and 
so on.

|                 Property functions                 |
|:--------------------------------------------------:|
|      [getProperty](docstrings.md#getproperty)      |
| [getPropertyValue](docstrings.md#getpropertyvalue) |
|   [changeProperty](docstrings.md#changeproperty)   |
|      [sendMessage](docstrings.md#sendmessage)      |


## Properties, atoms and hints values

These values are accessible through `Props` class (ewmhlib.Props.*). 
They include all properties, atoms and hints values recognized by EWMH specs, so makes it easier 
to find, enumerate or use them.

They have been organized in different subclasses, according to their type or when they should be used:

|         Properties, atoms and hints          |
|:--------------------------------------------:|
|          [Root](docstrings.md#root)          |
| [DesktopLayout](docstrings.md#desktoplayout) |
|        [Window](docstrings.md#window)        |
|    [WindowType](docstrings.md#windowtype)    |
|         [State](docstrings.md#state)         |
|   [StateAction](docstrings.md#stateaction)   |
|    [MoveResize](docstrings.md#moveresize)    |
|    [DataFormat](docstrings.md#dataformat)    |
|          [Mode](docstrings.md#mode)          |
|     [StackMode](docstrings.md#stackmode)     |
|    [HintAction](docstrings.md#hintaction)    |


## Data Structs

Aimed to facilitate understanding and handling complex reply data structures and fields.

|                 Data Structs                 |
|:--------------------------------------------:|
|  [DisplaysInfo](docstrings.md#displaysinfo)  |
|   [ScreensInfo](docstrings.md#screensinfo)   |
|       [WmHints](docstrings.md#wmhints)       |
| [WmNormalHints](docstrings.md#wmnormalhints) |


## Install <a name="install"></a>

To install this module on your system, you can use pip: 

    pip3 install ewmhlib

or

    python3 -m pip install ewmhlib

Alternatively, you can download the wheel file (.whl) available in the [Download page](https://pypi.org/project/EWMHlib/#files) and the [dist folder](https://github.com/Kalmat/EWMHlib/tree/master/dist), and run this (don't forget to replace 'x.xx' with proper version number):

    pip install EWMHlib-x.xx-py3-none-any.whl

You may want to add `--force-reinstall` option to be sure you are installing the right dependencies version.

Then, you can use it on your own projects just importing it:

    import ewmhlib

## Support <a name="support"></a>

In case you have a problem, comments or suggestions, do not hesitate to [open issues](https://github.com/Kalmat/EWMHlib/issues) on the [project homepage](https://github.com/Kalmat/EWMHlib)

## Using this code <a name="using"></a>

If you want to use this code or contribute, you can either:

* Create a fork of the [repository](https://github.com/Kalmat/EWMHlib), or 
* [Download the repository](https://github.com/Kalmat/EWMHlib/archive/refs/heads/master.zip), uncompress, and open it on your IDE of choice (e.g. PyCharm)

Be sure you install all dependencies described on "docs/requirements.txt" by using pip

## Test <a name="test"></a>

To test this module on your own system, cd to "tests" folder and run:

    python3 test_ewmhlib.py
 

## List of window managers that support Extended Window Manager Hints

An (likely) incomplete list of EWMH-compliant window managers is (via Wikipedia, [here](https://en.wikipedia.org/wiki/Extended_Window_Manager_Hints) and [here](https://en.wikipedia.org/wiki/Comparison_of_X_window_managers#General_information)):

|         Name         |  Comments   |
|:--------------------:|:-----------:|
|         aewm         |             |
|       awesome        |             |
|       Blackbox       |     (1)     |
|        bspwm         |   Partial   |
|         CTWM         |     (2)     |
|        Compiz        |             |
|       echinus        |             |
|        edewm         |             |
|    Enlightenment     |             |
|        evilwm        | Partial (3) |
|         EXWM         |   Partial   |
|       Fluxbox        |             |
|         FVWM         |             |
|       goomwwm        |             |
|     herbstluftwm     |             |
|          i3          |             |
|        IceWM         |             |
|     interfacewm      |             |
|         JWM          |             |
|      KWin (KDE)      |             |
|        LeftWM        |             |
|        Marco         |             |
|       Matchbox       |             |
|   Metacity (GNOME)   |             |
| Mutter (GNOME/MeeGo) |             |
|        Notion        |             |
|       Openbox        |             |
|        PekWM         |   Partial   |
|        PlayWM        |             |
|        Qtile         |             |
|       Sawfish        |   Partial   |
|       spectrwm       |             |
|        subtle        |             |
|     Window Maker     |   Partial   |
|        Wingo         |             |
|         WMFS         |             |
|         wmii         |             |
|     Xfwm (Xfce)      |             |
|        xmonad        |     (4)     |

(1) Through 0.65 / from 0.70

(2) As of 4.0.0

(3) Releases following and including version 1.1.0 follow the EWMH standard

(4) Must activate EWMH (XMonad.Hooks.EwmhDesktops)
