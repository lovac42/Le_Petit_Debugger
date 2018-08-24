# -*- coding: utf-8 -*-
# Copyright: (C) 2018 Lovac42
# Support: https://github.com/lovac42/Le_Petit_Debugger
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Version: 0.0.1


import aqt, sys
from aqt import mw
from anki.hooks import addHook
from aqt.qt import *

from anki import version
ANKI21 = version.startswith("2.1.")


class DebugConsole:
    def __init__(self):
        self.onDebug()

    def show(self):
        self.form.log.setPlainText('')
        self.dialog.show()

    def onDebug(self):
        self.dialog = QDialog()
        d = self.dialog
        self.form = aqt.forms.debug.Ui_Dialog()
        self.form.setupUi(d)
        s = QShortcut(QKeySequence("ctrl+return"), d)
        s.activated.connect(self.onDebugRet)
        s = QShortcut(QKeySequence("ctrl+shift+return"), d)
        s.activated.connect(self.onDebugPrint)
        s = QShortcut(QKeySequence("ctrl+alt+return"), d)
        s.activated.connect(self.onDebugJS)

    def onDebugPrint(self):
        self.form.text.setPlainText("pp(%s)" % self.form.text.toPlainText())
        self.onDebugRet()

    def onDebugJS(self):
        self.form.text.setPlainText('js("""%s""")' % self.form.text.toPlainText())
        self.onDebugRet()

    def onDebugRet(self):
        import pprint, traceback
        text = self.form.text.toPlainText()
        js = self.evalJS
        pp = pprint.pprint
        self._captureOutput(True)
        try:
            exec(text)
        except:
            self._output += traceback.format_exc()
        self._captureOutput(False)
        buf = ""
        for c, line in enumerate(text.strip().split("\n")):
            if c == 0:
                buf += ">>> %s\n" % line
            else:
                buf += "... %s\n" % line
        self.log(buf + (self._output or "<no output>"))

    def _captureOutput(self, on):
        console = self
        class Stream(object):
            def write(self, data):
                console._output += data
        if on:
            self._output = ""
            self._oldStderr = sys.stderr
            self._oldStdout = sys.stdout
            s = Stream()
            sys.stderr = s
            sys.stdout = s
        else:
            sys.stderr = self._oldStderr
            sys.stdout = self._oldStdout

    def evalJS(self,js):
         if ANKI21:
             mw.web.page().runJavaScript(js)
         else:
             mw.web.page().mainFrame().evaluateJavaScript(js)

    def log(self,msg):
        try:
            self.form.log.appendPlainText(msg)
        except UnicodeDecodeError:
            self.form.log.appendPlainText(_("<non-unicode text>"))
        self.form.log.ensureCursorVisible()
