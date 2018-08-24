# -*- coding: utf-8 -*-
# Copyright: (C) 2018 Lovac42
# Support: https://github.com/lovac42/Le_Petit_Debugger
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Version: 0.0.1


from aqt import mw
from anki.hooks import addHook
from .utils import addMenuItem


class Info:
    def __init__(self):
        addMenuItem('Debug', 'print card info', self.log)

    def log(self):
        mw.db.log("Info:")
        self.model()
        self.state()
        # self.help()
        # self.fields(mw.reviewer.card.note())

    def state(self):
        mw.db.log("""  mw.state = '%s'
  mw.reviewer.state = '%s'
  mw.reviewer.card = %s
"""%(mw.state,mw.reviewer.state,str(mw.reviewer.card)) )

    def model(self):
        mw.db.log('  model = '+mw.reviewer.card.model()['name'])

    def fields(self, note):
        for f in note.model()['flds']:
            mw.db.log(f['name']+':'+note[f['name']])

    def help(self):
        mw.db.log("""
Type: 0=new, 1=learning, 2=due
Queue: same as above, and:
       -1=suspended, -2=user buried, -3=sched buried
Due is used differently for different queues.
- new queue: note id or random int
- rev queue: integer day
- lrn queue: integer timestamp
""")

mw.db.info=Info()
