# EWMHlib
[![CI](https://github.com/Kalmat/EWMHlib/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/Kalmat/EWMHlib/actions/workflows/ci.yml)
[![PyPI version](https://badge.fury.io/py/EWMHlib.svg)](https://badge.fury.io/py/EWMHlib)
[![Documentation Status](https://readthedocs.org/projects/ewmhlib/badge/?version=latest)](https://ewmhlib.readthedocs.io/en/latest/?badge=latest)
[![Downloads](https://static.pepy.tech/badge/ewmhlib/month)](https://pepy.tech/project/ewmhlib)
[![Stars](https://img.shields.io/github/stars/Kalmat/EWMHlib?style=flat)](https://github.com/Kalmat/EWMHlib/stargazers)
[![License](https://img.shields.io/badge/license-BSD%203--Clause-blue)](LICENSE.txt)

A complete [EWMH](https://specifications.freedesktop.org/wm-spec/latest/) (Extended Window Manager Hints) implementation in Python 3 and python-xlib. Provides full, Pythonic access to the EWMH spec — query and control any compliant Window Manager, manage window hints, and subscribe to X events.

**Tested on:** Ubuntu/GNOME · Mint/Cinnamon · Manjaro/KDE · Raspbian/LXDE

> **⚠️ Wayland note:** The new protocol used by GNOME in Ubuntu (Wayland) is not EWMH-compliant. This module is likely not working under Wayland.

---

## Why EWMHlib?

- **Complete and updated spec coverage** — all EWMH properties, atoms, states, window types, hints and messages are implemented and accessible.
- **Full read _and_ write support** — not just querying, but sending messages and changing properties through the Window Manager.
- **Typed, structured API** — methods return typed values (integers, strings, named tuples) instead of raw Xlib structs, with `text=True` variants where atom names are more useful than atom ids.
- **Multi-display and multi-screen support** — convenience functions to enumerate displays, screens and roots, going beyond the default display assumption.
- **Window hints management** — read and write `WM_HINTS` and `WM_NORMAL_HINTS`, including urgency, icon, input model and size constraints.
- **Event watching** — subscribe to any X event on a window via a background watchdog thread and a callback, without managing the event loop yourself.
- **Low-level escape hatch** — module-level `getProperty` / `changeProperty` / `sendMessage` functions for custom or non-standard properties, with built-in atom resolution and reply parsing.

---

## Quick start

```python
from ewmhlib import EwmhRoot, EwmhWindow

# --- Root-level operations ---
root = EwmhRoot()

# Get the active (focused) window
win_id = root.getActiveWindow()

# List all open windows
all_windows = root.getClientList()

# How many virtual desktops are there?
n = root.getNumberOfDesktops()
print(f"{n} desktops available")

# Switch to desktop 1
root.setCurrentDesktop(1)

# --- Window-level operations ---
if win_id:
    win = EwmhWindow(win_id)

    # Read title and PID
    print(win.getName())
    print(win.getPid())

    # Move the window to desktop 2
    win.setDesktop(2)

    # Maximize it
    win.setMaximized(True, True)

    # Focus it
    win.setActive()

    # Close it
    win.setClosed()
```

### Watching for events

```python
import time
import Xlib.X
from ewmhlib import EwmhRoot, EwmhWindow

root = EwmhRoot()
win_id = root.getActiveWindow()

if win_id:
    win = EwmhWindow(win_id)

    def on_event(event):
        print("Event received:", event)

    win.extensions.checkEvents.start(
        [Xlib.X.ConfigureNotify, Xlib.X.ClientMessage],
        Xlib.X.StructureNotifyMask | Xlib.X.SubstructureNotifyMask,
        on_event
    )

    print("Move or resize the window. Press Ctrl-C to stop.")
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass

    win.extensions.checkEvents.stop()
```

---

## Ecosystem

EWMHlib is used as the Linux backend for [PyWinCtl](https://github.com/Kalmat/PyWinCtl), a cross-platform window control library.

---

## Table of Contents

- [General functions and variables](#general-functions-and-variables)
  - [General objects](#general-objects)
  - [General functions](#general-functions)
- [EwmhRoot — Root queries, changes and messages](#ewmhroot--root-queries-changes-and-messages)
- [EwmhWindow — Window queries, changes and messages](#ewmhwindow--window-queries-changes-and-messages)
  - [EwmhWindow Extensions: Geometry, Hints, Protocols and Events](#ewmhwindow-extensions-geometry-hints-protocols-and-events)
- [Properties and Messages functions](#properties-and-messages-functions)
- [Properties, atoms and hints values](#properties-atoms-and-hints-values)
- [Data Structs](#data-structs)
- [Install](#install)
- [Support / Contributing](#support--contributing)
- [Test](#test)
- [List of EWMH-compliant window managers](#list-of-ewmh-compliant-window-managers)

---

## General functions and variables

These are module-level — no class instantiation needed.

### General objects

Provide direct access to the default display, screen and root, ready to use in any Xlib-related function.

| Object | Description |
|--------|-------------|
| `defaultDisplay` | Default X display connection |
| `defaultScreen` | Default screen |
| `defaultRoot` | Default root window |

### General functions

Useful for multi-display or multi-screen setups. In most single-display scenarios the objects above are sufficient.

| Function | Description |
|----------|-------------|
| [getDisplaysInfo()](docs/docstrings.md#getdisplaysinfo) | Get info on all present displays, including screens and roots |
| [getDisplayFromRoot()](docs/docstrings.md#getdisplayfromroot) | Get display connection, screen and root from a root id |
| [getDisplayFromWindow()](docs/docstrings.md#getdisplayfromwindow) | Get display connection, screen and root from a window id |
| [getRoots()](docs/docstrings.md#getroots) | Get all root window objects |

---

## EwmhRoot — Root queries, changes and messages

Class to access root window features.

For the default root, use the convenience object `defaultRootWindow` — it gives instant access to all root methods without instantiating anything (equivalent to `myRoot = EwmhRoot()`).

To instantiate `EwmhRoot` for a specific root, pass its id. You can obtain it in several ways:

- You already have a root → pass `root.id`
- You want to search across roots → use `getDisplaysInfo()` to enumerate all roots and pick the desired one
- You have a window → use `getDisplayFromWindow(window.id)` to retrieve the associated root
- No argument → retrieves the default display and root

Note: although a regular window and a root window share the same type, `EwmhRoot` methods are not intended for regular windows.

### EwmhRoot methods

| Method | Description |
|--------|-------------|
| [getSupportedHints()](docs/docstrings.md#getsupportedhints) | List hints supported by the Window Manager |
| [getClientList()](docs/docstrings.md#getclientlist) | List managed windows in mapping order (oldest first) |
| [getClientListStacking()](docs/docstrings.md#getclientliststacking) | List managed windows in stacking order (bottom to top) |
| [getNumberOfDesktops()](docs/docstrings.md#getnumberofdesktops) | Get the number of virtual desktops |
| [setNumberOfDesktops()](docs/docstrings.md#setnumberofdesktops) | Request a change in the number of virtual desktops |
| [getDesktopGeometry()](docs/docstrings.md#getdesktopgeometry) | Get the common size of all desktops |
| [setDesktopGeometry()](docs/docstrings.md#setdesktopgeometry) | Request a change in the desktop geometry |
| [getDesktopViewport()](docs/docstrings.md#getdesktopviewport) | Get the top-left corner of each desktop's viewport |
| [setDesktopViewport()](docs/docstrings.md#setdesktopviewport) | Request a change in the current desktop viewport |
| [getCurrentDesktop()](docs/docstrings.md#getcurrentdesktop) | Get the index of the current desktop |
| [setCurrentDesktop()](docs/docstrings.md#setcurrentdesktop) | Switch to a different virtual desktop |
| [getDesktopNames()](docs/docstrings.md#getdesktopnames) | Get the names of all virtual desktops |
| [getActiveWindow()](docs/docstrings.md#getactivewindow) | Get the id of the currently active (focused) window |
| [getWorkArea()](docs/docstrings.md#getworkarea) | Get the work area geometry for each desktop |
| [getSupportingWMCheck()](docs/docstrings.md#getsupportingwmcheck) | Check whether a compliant Window Manager is active |
| [getVirtualRoots()](docs/docstrings.md#getvirtualroots) | Get the list of virtual root window ids |
| [setDesktopLayout()](docs/docstrings.md#setdesktoplayout) | Set the pager's virtual desktop layout |
| [getShowingDesktop()](docs/docstrings.md#getshowingdesktop) | Check whether "show desktop" mode is active |
| [setShowingDesktop()](docs/docstrings.md#setshowingdesktop) | Enter or exit "show desktop" mode |
| [setClosed()](docs/docstrings.md#setclosed) | Request the Window Manager to close a window |
| [setMoveResize()](docs/docstrings.md#setmoveresize) | Move and/or resize a window |
| [setWmMoveResize()](docs/docstrings.md#setwmmoveresize) | Initiate interactive move/resize controlled by the WM |
| [setWmStacking()](docs/docstrings.md#setwmstacking) | Restack a window relative to a sibling (pager use) |
| [requestFrameExtents()](docs/docstrings.md#requestframeextents) | Ask the WM to estimate frame extents before mapping |

WM_PROTOCOLS messages (PING/SYNC) are available via the `wmProtocols` subclass (`EwmhRoot.wmProtocols.*`):

| Method | Description |
|--------|-------------|
| [ping()](docs/docstrings.md#ping) | Send a WM_PING to check if a client is still responsive |
| [sync()](docs/docstrings.md#sync) | Synchronize WM frame repaints with the client window |

### EwmhRoot variables

These are accessible as `EwmhRoot.*` and can be passed directly to python-xlib. In most cases they match the default general variables above.

| Variable | Description |
|----------|-------------|
| `display` | XDisplay connection the root belongs to |
| `screen` | Screen the root belongs to (Struct) |
| `root` | Root as an X Window object |
| `id` | Root window id |

---

## EwmhWindow — Window queries, changes and messages

Class to access application window features.

Only a window id is needed to instantiate. You can obtain it in several ways:

- Use an external module: `pywinctl.getAllWindowsWithTitle(title)` or `pywinctl.getActiveWindow()`
- Retrieve it from your own application: PyQt's `winId()` or Tkinter's `frame()`

Note: although a root is also a window, most of these methods will not work with a root.

### EwmhWindow methods

| Method | Description |
|--------|-------------|
| [getName()](docs/docstrings.md#getname) | Get the window title (_NET_WM_NAME) |
| [setName()](docs/docstrings.md#setname) | Set the window title |
| [getVisibleName()](docs/docstrings.md#getvisiblename) | Get the visible name shown by the WM (may differ from getName) |
| [setVisibleName()](docs/docstrings.md#setvisiblename) | Set the visible name |
| [getIconName()](docs/docstrings.md#geticonname) | Get the window icon name |
| [setIconName()](docs/docstrings.md#seticonname) | Set the window icon name |
| [getVisibleIconName()](docs/docstrings.md#getvisibleiconname) | Get the visible icon name shown by the WM |
| [setVisibleIconName()](docs/docstrings.md#setvisibleiconname) | Set the visible icon name |
| [getDesktop()](docs/docstrings.md#getdesktop) | Get the desktop index this window is on (0xFFFFFFFF = all desktops) |
| [setDesktop()](docs/docstrings.md#setdesktop) | Move the window to a specific desktop |
| [getWmWindowType()](docs/docstrings.md#getwmwindowtype) | Get the functional window type (NORMAL, DIALOG, DOCK, etc.) |
| [setWmWindowType()](docs/docstrings.md#setwmwindowtype) | Change the window type |
| [getWmState()](docs/docstrings.md#getwmstate) | Get the list of current window states |
| [changeWmState()](docs/docstrings.md#changewmstate) | Add, remove or toggle a window state |
| [setMaximized()](docs/docstrings.md#setmaximized) | Set or unset horizontal/vertical maximized states |
| [setMinimized()](docs/docstrings.md#setminimized) | Iconify (minimize) the window |
| [getAllowedActions()](docs/docstrings.md#getallowedactions) | Get the list of user actions currently allowed on this window |
| [getStrut()](docs/docstrings.md#getstrut) | Get reserved screen-border space (legacy, see getStrutPartial) |
| [setStrut()](docs/docstrings.md#setstrut) | Set reserved screen-border space |
| [getStrutPartial()](docs/docstrings.md#getstrutpartial) | Get detailed reserved space at each screen border |
| [getIconGeometry()](docs/docstrings.md#geticongeometry) | Get the geometry of the window's taskbar icon |
| [getPid()](docs/docstrings.md#getpid) | Get the process id (PID) of the window's owner |
| [getHandledIcons()](docs/docstrings.md#gethandledicons) | Check whether the pager is handling icons for this window |
| [getUserTime()](docs/docstrings.md#getusertime) | Get the timestamp of last user activity in this window |
| [getFrameExtents()](docs/docstrings.md#getframeextents) | Get the WM frame extents (left, right, top, bottom) |
| [getOpaqueRegion()](docs/docstrings.md#getopaqueregion) | Get the fully-opaque rectangles within the window |
| [getBypassCompositor()](docs/docstrings.md#getbypasscompositor) | Check whether the compositor should be bypassed |
| [setActive()](docs/docstrings.md#setactive) | Activate (focus) this window |
| [setClosed()](docs/docstrings.md#setclosed-1) | Request the WM to close this window |
| [changeStacking()](docs/docstrings.md#changestacking) | Change this window's stacking position relative to siblings |
| [setMoveResize()](docs/docstrings.md#setmoveresize-1) | Move and/or resize this window |
| [setWmMoveResize()](docs/docstrings.md#setwmmoveresize-1) | Initiate interactive move/resize via the WM |
| [setWmStacking()](docs/docstrings.md#setwmstacking-1) | Restack this window (pager use) |
| [requestFrameExtents()](docs/docstrings.md#requestframeextents-1) | Ask WM to estimate frame extents before this window is mapped |

### EwmhWindow variables

| Variable | Description |
|----------|-------------|
| `display` | XDisplay connection the window belongs to |
| `screen` | Screen the window belongs to (Struct) |
| `root` | Root the window belongs to (X Window object) |
| `rootWindow` | Root the window belongs to (EwmhRoot object) |
| `XWindow` | X Window object associated with this window |
| `id` | Window id |

---

### EwmhWindow Extensions: Geometry, Hints, Protocols and Events

Low-level, non-EWMH window features — hints, protocols, and event monitoring — available via `EwmhWindow.extensions.*`.

| Method | Description |
|--------|-------------|
| [getWmHints()](docs/docstrings.md#getwmhints) | Get WM_HINTS (input model, icon, urgency, etc.) |
| [setWmHints()](docs/docstrings.md#setwmhints) | Set or update WM_HINTS |
| [getWmNormalHints()](docs/docstrings.md#getwmnormalhints) | Get WM_NORMAL_HINTS (size constraints, gravity, aspect) |
| [setWmNormalHints()](docs/docstrings.md#setwmnormalhints) | Set or update WM_NORMAL_HINTS |
| [getWmProtocols()](docs/docstrings.md#getwmprotocols) | Get the WM protocols supported by this window |
| [addWmProtocols()](docs/docstrings.md#addwmprotocols) | Add supported WM protocols |
| [delWmProtocols()](docs/docstrings.md#delwmprotocols) | Remove supported WM protocols |
| [CheckEvents](docs/docstrings.md#checkevents) | Watch for X events and invoke a callback |

`CheckEvents` runs a background watchdog thread. Control it with:

| Method | Description |
|--------|-------------|
| [start()](docs/docstrings.md#start) | Start watching for events (can be called again to update args) |
| [pause()](docs/docstrings.md#pause) | Pause the watchdog (resume by calling start() again) |
| [stop()](docs/docstrings.md#stop) | Stop and terminate the watchdog thread |

---

## Properties and Messages functions

These module-level functions let you query and control windows or roots directly, without instantiating `EwmhRoot` or `EwmhWindow`. They are closer to raw Xlib — more flexible for custom or non-standard use cases, but also more verbose. They simplify handling of atoms, replies and data format conversions.

| Function | Description |
|----------|-------------|
| [getProperty()](docs/docstrings.md#getproperty) | Retrieve a property from a window or root |
| [getPropertyValue()](docs/docstrings.md#getpropertyvalue) | Extract data from a retrieved property struct |
| [changeProperty()](docs/docstrings.md#changeproperty) | Set or change a property on a window or root |
| [sendMessage()](docs/docstrings.md#sendmessage) | Send a ClientMessage event to a window or root |

---

## Properties, atoms and hints values

All EWMH-defined properties, atoms and hint values are accessible through the `Props` class (`ewmhlib.Props.*`). They cover everything recognized by the spec, organized into subclasses by category so they're easy to discover and enumerate.

| Subclass | Description |
|----------|-------------|
| [Root](docs/docstrings.md#root) | Root window properties (client list, desktops, active window…) |
| [DesktopLayout](docs/docstrings.md#desktoplayout) | Desktop layout orientation and corner constants |
| [Window](docs/docstrings.md#window) | Per-window properties (name, desktop, PID, strut…) |
| [WindowType](docs/docstrings.md#windowtype) | Window type atoms (NORMAL, DIALOG, DOCK, TOOLBAR…) |
| [State](docs/docstrings.md#state) | Window state atoms (maximized, minimized, fullscreen…) |
| [StateAction](docs/docstrings.md#stateaction) | State change actions (ADD, REMOVE, TOGGLE) |
| [MoveResize](docs/docstrings.md#moveresize) | Move/resize direction and edge constants |
| [DataFormat](docs/docstrings.md#dataformat) | Property data format constants (8, 16, 32 bit) |
| [Mode](docs/docstrings.md#mode) | Property change mode (REPLACE, APPEND, PREPEND) |
| [StackMode](docs/docstrings.md#stackmode) | Window stacking modes (Above, Below, TopIf…) |
| [HintAction](docs/docstrings.md#hintaction) | Hint modification actions (KEEP, REMOVE, or new value) |

---

## Data Structs

Named tuples to help interpret the structured data returned by some methods.

| Struct | Description |
|--------|-------------|
| [DisplaysInfo](docs/docstrings.md#displaysinfo) | Display/screen/root info returned by getDisplaysInfo() |
| [ScreensInfo](docs/docstrings.md#screensinfo) | Per-screen info |
| [WmHints](docs/docstrings.md#wmhints) | WM_HINTS fields returned by getWmHints() |
| [WmNormalHints](docs/docstrings.md#wmnormalhints) | WM_NORMAL_HINTS fields returned by getWmNormalHints() |

---

## Install <a name="install"></a>

To install this module on your system, you can use pip:

    python -m pip install ewmhlib

or using uv:

    uv add ewmhlib

Alternatively, you can download the wheel file (.whl) available in the [Download page](https://pypi.org/project/EWMHlib/#files) and the [dist folder](https://github.com/Kalmat/EWMHlib/tree/master/dist), and run this (don't forget to replace 'x.xx' with proper version number):

    python -m pip install EWMHlib-x.xx-py3-none-any.whl

You may want to add `--force-reinstall` option to be sure you are installing the right dependencies version.

Then, you can use it on your own projects just importing it:

    import ewmhlib

## Support <a name="support"></a>

In case you have a problem, comments or suggestions, do not hesitate to [open issues](https://github.com/Kalmat/EWMHlib/issues) on the [project homepage](https://github.com/Kalmat/EWMHlib)

## Using this code <a name="using"></a>

If you want to use this code or contribute, you can either:

* Create a fork of the [repository](https://github.com/Kalmat/EWMHlib), or 
* [Download the repository](https://github.com/Kalmat/EWMHlib/archive/refs/heads/master.zip), uncompress, and open it on your IDE of choice (e.g. PyCharm)

Be sure you install all dev dependencies by running:

    uv sync

or
    python -m venv .venv
    python -m pip install -e . --group=dev

## Test <a name="test"></a>

To test this module on your own system, cd to "tests" folder and run:

    uv run test_ewmhlib.py

---

## List of EWMH-compliant window managers

A (likely) incomplete list of EWMH-compliant window managers (via Wikipedia, [here](https://en.wikipedia.org/wiki/Extended_Window_Manager_Hints) and [here](https://en.wikipedia.org/wiki/Comparison_of_X_window_managers#General_information)):

| Name | Notes |
|------|-------|
| aewm | |
| awesome | |
| Blackbox | (1) |
| bspwm | Partial |
| CTWM | (2) |
| Compiz | |
| echinus | |
| edewm | |
| Enlightenment | |
| evilwm | Partial (3) |
| EXWM | Partial |
| Fluxbox | |
| FVWM | |
| goomwwm | |
| herbstluftwm | |
| i3 | |
| IceWM | |
| interfacewm | |
| JWM | |
| KWin (KDE) | |
| LeftWM | |
| Marco | |
| Matchbox | |
| Metacity (GNOME) | |
| Mutter (GNOME/MeeGo) | |
| Notion | |
| Openbox | |
| PekWM | Partial |
| PlayWM | |
| Qtile | |
| Sawfish | Partial |
| spectrwm | |
| subtle | |
| Window Maker | Partial |
| Wingo | |
| WMFS | |
| wmii | |
| Xfwm (Xfce) | |
| xmonad | (4) |

(1) Through 0.65 / from 0.70  
(2) As of 4.0.0  
(3) Releases following and including version 1.1.0 follow the EWMH standard  
(4) Must activate EWMH (`XMonad.Hooks.EwmhDesktops`)
