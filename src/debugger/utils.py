# These functions are taken from: incremental-reading v3.8.3


# Copyright 2017-2018 Luo Li-Yan <joseph.lorimer13@gmail.com>
#
# Permission to use, copy, modify, and distribute this software for any purpose
# with or without fee is hereby granted, provided that the above copyright
# notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
# AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
# LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
# OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.

from __future__ import unicode_literals
from aqt import mw
from aqt.qt import *

def addMenu(fullName):
    if not hasattr(mw, 'customMenus'):
        mw.customMenus = {}

    if len(fullName.split('::')) == 2:
        menuName, subMenuName = fullName.split('::')
        hasSubMenu = True
    else:
        menuName = fullName
        hasSubMenu = False

    if menuName not in mw.customMenus:
        menu = QMenu('&' + menuName, mw)
        mw.customMenus[menuName] = menu
        mw.form.menubar.insertMenu(mw.form.menuTools.menuAction(),
                                   mw.customMenus[menuName])

    if hasSubMenu and (fullName not in mw.customMenus):
        subMenu = QMenu('&' + subMenuName, mw)
        mw.customMenus[fullName] = subMenu
        mw.customMenus[menuName].addMenu(subMenu)


def addMenuItem(menuName, text, function, keys=None, checkable=False):
    action = QAction(text, mw)
    action.setCheckable(checkable)

    if keys:
        action.setShortcut(QKeySequence(keys))

    action.triggered.connect(function)

    if menuName == 'File':
        mw.form.menuCol.addAction(action)
    elif menuName == 'Edit':
        mw.form.menuEdit.addAction(action)
    elif menuName == 'Tools':
        mw.form.menuTools.addAction(action)
    elif menuName == 'Plugins':
        mw.form.menuPlugins.addAction(action)
    elif menuName == 'Help':
        mw.form.menuHelp.addAction(action)
    else:
        addMenu(menuName)
        mw.customMenus[menuName].addAction(action)

    return action


def addShortcut(function, keys):
    shortcut = QShortcut(QKeySequence(keys), mw)
    shortcut.activated.connect(function)

