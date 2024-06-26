#!/usr/bin/python
# -*- coding: utf-8 -*-


__all__ = [
    "version", "displaysCount", "getDisplays", "getDisplaysInfo", "getRoots",
    "defaultDisplay", "defaultScreen", "defaultRoot", "defaultEwmhRoot",
    "getDisplayFromRoot", "getScreenFromRoot",
    "getDisplayFromWindow", "getScreenFromWindow", "getRootFromWindow",
    "getProperty", "getPropertyValue", "changeProperty", "sendMessage",
    "EwmhRoot", "EwmhWindow",
    "Props", "Structs"
]

__version__ = "0.2"


def version(numberOnly: bool = True):
    """Returns the current version of ewmhlib module, in the form ''x.x.xx'' as string"""
    return ("" if numberOnly else "EWMHlib-")+__version__


from ._main import (displaysCount, getDisplays, getDisplaysInfo, getRoots,
                    defaultDisplay, defaultScreen, defaultRoot, defaultEwmhRoot,
                    getDisplayFromRoot, getScreenFromRoot,
                    getDisplayFromWindow, getScreenFromWindow, getRootFromWindow,
                    getProperty, getPropertyValue, changeProperty, sendMessage,
                    EwmhRoot, EwmhWindow,
                    Props, Structs
                    )
