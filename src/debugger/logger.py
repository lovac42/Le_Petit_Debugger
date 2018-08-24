# -*- coding: utf-8 -*-
# Copyright: (C) 2018 Lovac42
# Support: https://github.com/lovac42/Le_Petit_Debugger
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Version: 0.0.1


import aqt
from aqt import mw
from aqt.qt import *

from anki import version
ANKI21 = version.startswith("2.1.")
if ANKI21:
    from PyQt5 import QtCore, QtGui, QtWidgets
else:
    from PyQt4 import QtCore, QtGui



class Logger:
    def __init__(self):
        self.dialog = QDialog()
        self.form = self.setupUi(self.dialog)

    def show(self):
        self.dialog.show()

    def log(self,msg):
        try:
            self.text.appendPlainText(msg)
        except UnicodeDecodeError:
            self.text.appendPlainText(_("<non-unicode text>"))

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 600)

        if ANKI21:
            self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
            self.text = QtWidgets.QPlainTextEdit(Dialog)
            self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
            self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close|QtWidgets.QDialogButtonBox.Help)
        else: #anki20
            self.verticalLayout = QtGui.QVBoxLayout(Dialog)
            self.text = QtGui.QPlainTextEdit(Dialog)
            self.buttonBox = QtGui.QDialogButtonBox(Dialog)
            self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close|QtGui.QDialogButtonBox.Help)

        self.verticalLayout.setObjectName("verticalLayout")
        self.text.setObjectName("text")
        self.verticalLayout.addWidget(self.text)

        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        Dialog.setWindowTitle(_("Console Output"))
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

