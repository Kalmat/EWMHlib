import sys
import time

import Xlib.protocol
import Xlib.X

sys.path.insert(0, "../src/")
from ewmhlib import Props, getDisplaysInfo, EwmhRoot, EwmhWindow


def main():
    print("ALL DISPLAYS")
    print(getDisplaysInfo())

    root = EwmhRoot()

    print("DESKTOP LAYOUT")
    print(root.getDesktopLayout())
    print("DESKTOP GEOMETRY")
    print(root.getDesktopGeometry())
    print("DESKTOP NAMES")
    print(root.getDesktopNames())
    print("DESKTOP VIEWPORT")
    print(root.getDesktopViewport())
    print("SHOWING DESKTOP")
    print(root.getShowingDesktop())
    print("SUPPORTING WM CHECK")
    print(root.getSupportingWMCheck())

    print("NUMBER OF DESKTOPS")
    print(root.getNumberOfDesktops())
    print("CURRENT DESKTOP")
    currDesktop = root.getCurrentDesktop()
    print(currDesktop)
    print("CHANGE DESKTOP")
    root.setCurrentDesktop(1)
    time.sleep(3)
    print(root.getCurrentDesktop())
    print("BACK TO ORIGINAL DESKTOP")
    if currDesktop is None:
        currDesktop = 0
    root.setCurrentDesktop(currDesktop)
    time.sleep(3)
    print(root.getCurrentDesktop())

    print("SUPPORTED HINTS")
    print(root.getSupportedHints(True))

    print("CLIENT LIST")
    print(root.getClientList())
    print("CLIENT LIST STACKING")
    print(root.getClientListStacking())

    w = root.getActiveWindow()
    if w:
        print("REQ FRAME EXTENTS")
        print(root.requestFrameExtents(w))
        win = EwmhWindow(w)
        name = win.getName()
        print("NAME", name)
        visName = win.getVisibleName()
        if visName is not None:
            print("VISIBLE NAME", visName)
            win.setVisibleName("This is a test")
            print("VISIBLE & NAME:", win.getVisibleName(), win.getName())
            win.setVisibleName(visName)
            print("VISIBLE & NAME:", win.getVisibleName(), win.getName())
        else:
            win.setName("This is a test")
            print("NAME & VISIBLE:", win.getName(), win.getVisibleName())
            win.setName(name if name else "")
            print("NAME & VISIBLE:", win.getName(), win.getVisibleName())
        print("TYPE", win.getWmWindowType())
        print("TYPE STR", win.getWmWindowType(text=True))
        print("STATE", win.getWmState())
        print("STATE STR", win.getWmState(text=True))
        print("ALLOWED ACTIONS", win.getAllowedActions(True))
        print("PID", win.getPid())
        print("FRAME EXT", win.getFrameExtents())
        # These are returning None... is it OK???
        print("STRUT", win.getStrut())
        print("STRUT PARTIAL", win.getStrutPartial())
        print("ICON GEOM", win.getIconGeometry())
        print("HANDLED ICONS", win.getHandledIcons())
        print("USER TIME", win.getUserTime())

        def callback(event: Xlib.protocol.rq.Event):
            print("EVENT RECEIVED", event)

        win.extensions.checkEvents.start([Xlib.X.ConfigureNotify, Xlib.X.ConfigureRequest, Xlib.X.ClientMessage],
                                         Xlib.X.StructureNotifyMask | Xlib.X.SubstructureNotifyMask,
                                         callback)

        print("MOVING/RESIZING")
        root.setMoveResize(w, x=100, y=100, width=800, height=600, userAction=True)  # Equivalent to win.setMoveResize()
        print("BELOW ON")
        win.changeWmState(Props.StateAction.ADD, Props.State.BELOW)
        time.sleep(4)
        print("BELOW OFF")
        win.changeWmState(Props.StateAction.REMOVE, Props.State.BELOW)
        time.sleep(4)
        print("DESKTOP")
        win.setWmWindowType(Props.WindowType.DESKTOP)
        time.sleep(4)
        print("NORMAL")
        win.setWmWindowType(Props.WindowType.NORMAL)
        print("MAX HORZ ON")
        win.setMaximized(True, False)
        time.sleep(4)
        print("MAX HORZ OFF")
        win.setMaximized(False, False)
        time.sleep(4)
        print("MAX")
        win.setMaximized(True, True)
        time.sleep(4)
        print("MAX HORZ OFF")
        win.setMaximized(False, True)
        time.sleep(4)
        print("MAX OFF")
        win.setMaximized(False, False)
        time.sleep(4)
        print("ICONIFY")
        win.setMinimized()
        time.sleep(4)
        print("RESTORE")
        win.setActive()
        time.sleep(4)
        print("END EVENT LOOP")
        win.extensions.checkEvents.stop()

        print("WM HINTS")
        hints = win.extensions.getWmHints()
        print(hints)
        win.extensions.setWmHints(icon_pixmap=win.xWindow.create_pixmap(32, 32, 1))
        print(win.extensions.getWmHints())
        print("WM NORMAL HINTS")
        normal_hints = win.extensions.getWmNormalHints()
        if normal_hints is not None:
            print(normal_hints)
            print("AVOID RESIZE")
            win.extensions.setWmNormalHints(min_width=600, max_width=600, min_height=400, max_height=400)
            time.sleep(4)
            print(win.extensions.getWmNormalHints())
            win.extensions.setWmNormalHints(min_width=normal_hints["min_width"], max_width=normal_hints["max_height"], min_height=normal_hints["min_height"], max_height=normal_hints["max_height"])
            print(win.extensions.getWmNormalHints())
        print("WM PROTOCOLS")
        print(win.extensions.getWmProtocols(True))
        print("REQUEST CLOSE")
        root.setClosed(win.id)  # equivalent to w.setClosed(), but accepts any window id


if __name__ == "__main__":
    main()
