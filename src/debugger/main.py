# -*- coding: utf-8 -*-
# Copyright: (C) 2018 Lovac42
# Support: https://github.com/lovac42/Le_Petit_Debugger
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Version: 0.0.1


import aqt
from aqt import mw
from .utils import addMenuItem
from .debug import DebugConsole
from .logger import Logger

from anki import version
ANKI21 = version.startswith("2.1.")


class Debugger:
    def __init__(self):
        self.editor=DebugConsole()
        addMenuItem('Debug', 'Show Console', self.show)
        addMenuItem('Debug::Switch view', 'to Editor', lambda:self.switch('Editor'))
        addMenuItem('Debug::Switch view', 'to DebugConsole', self.switch)

        #Replace Debug Console shortcuts
        if not ANKI21:
            mw.debugShortcut.activated.disconnect(mw.onDebug)
            mw.debugShortcut.activated.connect(self.show)


    def switch(self, view=None):
        if view=='Editor':
            self.editor=Logger()
        else:
            self.editor=DebugConsole()
        self.show()

    def show(self):
        self.editor.show()

    def log(self,msg):
        self.editor.log(msg)


mw.db=Debugger()
