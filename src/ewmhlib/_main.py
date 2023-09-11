#!/usr/bin/python
# -*- coding: utf-8 -*-

from ._ewmhlib import (displaysCount, getDisplays, getDisplaysInfo, getRoots,
                       defaultDisplay, defaultScreen, defaultRoot, defaultEwmhRoot,
                       getDisplayFromRoot, getScreenFromRoot,
                       getDisplayFromWindow, getScreenFromWindow, getRootFromWindow,
                       getProperty, getPropertyValue, changeProperty, sendMessage,
                       EwmhRoot, EwmhWindow
                       )
from . import _props as Props
from . import _structs as Structs
