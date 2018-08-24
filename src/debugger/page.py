# -*- coding: utf-8 -*-
# Copyright: (C) 2018 Lovac42
# Support: https://github.com/lovac42/Le_Petit_Debugger
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Version: 0.0.1


import re
from aqt import mw
from aqt.utils import getText, showText
from anki.utils import json
# from aqt.qt import *
from .utils import addMenuItem

from anki import version
ANKI21 = version.startswith("2.1.")


class PageView:
    def __init__(self):
        addMenuItem('Debug::Web', 'eval JS', self.eval)

        addMenuItem('Debug::Web', 'show QA Div', self.printQA)
        addMenuItem('Debug::Web', 'show Body', self.printBody)
        addMenuItem('Debug::Web', 'show Head', self.printHead)
        addMenuItem('Debug::Web', 'show Page', self.printPage)
        addMenuItem('Debug::Web', 'show Toolbar', self.printToolbar)
        addMenuItem('Debug::Web', 'show Bottom Toolbar', self.printBottomToolbar)

        addMenuItem('Debug::Web', 'append to QA Div', self.appendQA)
        addMenuItem('Debug::Web', 'insert to QA Div', lambda:self.appendQA(True))
        addMenuItem('Debug::Web', 'replace QA Div', self.injectQA)
        addMenuItem('Debug::Web', 'replace Page', self.injectPage)
        addMenuItem('Debug::Web', 'replace Toolbar', self.injectToolbar)
        addMenuItem('Debug::Web', 'replace Bottom Toolbar', self.injectBottomToolbar)


    def eval(self,js=None):
        if not js:
            js,ok = getText('Enter text to eval:')
            if not ok: return

        if ANKI21:
            mw.web.page().runJavaScript(js, self._print)
        else:
            html=mw.web.page().mainFrame().evaluateJavaScript(js)
            self._print(html)

    def toHtml(self, web):
        if ANKI21:
            web.page().runJavaScript('document.body.parentNode.outerHTML;', self._print)
        else:
            html=web.page().mainFrame().toHtml()
            self._print(html)

    def _print(self, html):
        if not html: return
        # mw.db.log(html)
        showText(html)


    def printToolbar(self):
        self.toHtml(mw.toolbar.web)

    def printBottomToolbar(self):
        self.toHtml(mw.bottomWeb)

    def printPage(self):
        self.toHtml(mw.web)

    def printBody(self):
        self.eval("document.body.innerHTML;")

    def printHead(self):
        self.eval("document.head.innerHTML;")

    def printQA(self):
        self.eval("document.getElementById('qa').innerHTML;")


    def appendQA(self,prefix=False):
        newData,ok = getText('Enter HTML:')
        if not ok: return

        js="document.getElementById('qa').innerHTML;"
        if ANKI21: #async
            s=self
            def asyncAppend(qa):
                if prefix:
                    s.injectQA(newData+qa)
                else:
                    s.injectQA(qa+newData)
            mw.web.page().runJavaScript(js,asyncAppend)
        else:
            qa=mw.web.page().mainFrame().evaluateJavaScript(js)
            if prefix:
                self.injectQA(newData+qa)
            else:
                self.injectQA(qa+newData)

    def injectQA(self, html=None):
        if not html:
            html,ok = getText('Enter HTML:')
            if not ok: return
        js=("document.getElementById('qa').innerHTML=%s"%json.dumps(html))
        if ANKI21:
            mw.web.page().runJavaScript(js)
        else:
            html=mw.web.page().mainFrame().evaluateJavaScript(js)

    def injectToolbar(self):
        html,ok = getText('Enter HTML:')
        if ok: mw.toolbar.web.setHtml(html)

    def injectBottomToolbar(self):
        html,ok = getText('Enter HTML:')
        if ok: mw.bottomWeb.setHtml(html)

    def injectPage(self):
        html,ok = getText('Enter HTML:')
        if ok: mw.web.setHtml(html)


mw.db.page=PageView()
