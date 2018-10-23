# -*- coding: utf-8 -*-
# Copyright: (C) 2018 Lovac42
# Support: https://github.com/lovac42/Le_Petit_Debugger
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Version: 0.0.2


import sys
from aqt import mw
from .utils import addMenuItem


class Monitor:
    monitor=False

    def __init__(self):
        addMenuItem('Debug', 'Monitor STDOUT + STDERR', self.toggle, checkable=True)

    def toggle(self):
        self.monitor=not self.monitor
        mw.db.log("monitoring STDOUT/ERR is turned "+('on' if self.monitor else 'off'))
        class Stream(object):
            def write(self, data):
                mw.db.log(data)
        if self.monitor:
            s = Stream()
            self._oldStdout = sys.stdout
            self._oldStderr = sys.stderr
            sys.stdout = s
            sys.stderr = s
        else:
            sys.stderr = self._oldStderr
            sys.stdout = self._oldStdout

mw.db.monitor=Monitor()
