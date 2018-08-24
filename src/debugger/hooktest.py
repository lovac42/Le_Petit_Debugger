# -*- coding: utf-8 -*-
# Copyright: (C) 2018 Lovac42
# Support: https://github.com/lovac42/Le_Petit_Debugger
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Version: 0.0.1


from aqt import mw
from anki.hooks import addHook
from .utils import addMenuItem


#TODO: Add 2.1 Hooks
class HookTest:

    #Flag: [ Bool, Message ]
    hookers={
        'ALL':[False,'All'],
        'R':[False,'reset'],
        'Q':[False,'showQuestion'],
        'A':[False,'showAnswer'],
        'NC':[False,'noteChanged'],
        'BSC':[False,'beforeStateChange'],
        'ASC':[False,'afterStateChange'],
        'PL':[False,'profileLoaded'],
        'UP':[False,'unloadProfile'],
        'US':[False,'undoState'],
        'CL':[False,'colLoading'],
        'L':[False,'leech'],
        'PQA':[False,'prepareQA'], #v2.1
        # 'ND':[False,'newDeck'],
        # 'NT':[False,'newTag'],
        # 'NM':[False,'newModel'],
        # 'SCH':[False,'search'],
        # 'RN':[False,'remNotes'],
        # 'H':[False,'httpSend'],
        # 'S':[False,'sync'],
        # 'SM':[False,'syncMsg'],
        # 'BSM':[False,'browser.setupMenus'],
        # 'CMC':[False,'currentModelChanged'],
        # 'RC':[False,'reviewCleanup'],
        # 'RCME':[False,'Reviewer.contextMenuEvent'],
    }


    def __init__(self):
        addMenuItem('Debug::Log Hookers', self.hookers['ALL'][1], lambda:self.toggle('ALL'))
        addMenuItem('Debug::Log Hookers', self.hookers['R'][1], lambda:self.toggle('R'))
        addMenuItem('Debug::Log Hookers', self.hookers['Q'][1], lambda:self.toggle('Q'))
        addMenuItem('Debug::Log Hookers', self.hookers['A'][1], lambda:self.toggle('A'))
        addMenuItem('Debug::Log Hookers', self.hookers['PQA'][1], lambda:self.toggle('PQA')) #v2.1
        addMenuItem('Debug::Log Hookers', self.hookers['NC'][1], lambda:self.toggle('NC'))
        addMenuItem('Debug::Log Hookers', self.hookers['BSC'][1], lambda:self.toggle('BSC'))
        addMenuItem('Debug::Log Hookers', self.hookers['ASC'][1], lambda:self.toggle('ASC'))
        addMenuItem('Debug::Log Hookers', self.hookers['PL'][1], lambda:self.toggle('PL'))
        addMenuItem('Debug::Log Hookers', self.hookers['UP'][1], lambda:self.toggle('UP'))
        addMenuItem('Debug::Log Hookers', self.hookers['US'][1], lambda:self.toggle('US'))
        addMenuItem('Debug::Log Hookers', self.hookers['CL'][1], lambda:self.toggle('CL'))
        addMenuItem('Debug::Log Hookers', self.hookers['L'][1], lambda:self.toggle('L'))



        addHook('reset', self.onReset)
        addHook('showQuestion', self.onShowQuestion)
        addHook('showAnswer', self.onShowAnswer)
        addHook('noteChanged', self.onNoteChanged)
        addHook('profileLoaded', self.onProfileLoaded)
        addHook('unloadProfile', self.onUnloadProfile)
        addHook('beforeStateChange', self.onBeforeStateChange)
        addHook('afterStateChange', self.onAfterStateChange)
        addHook("undoState", self.onUndoState)
        addHook("colLoading", self.onColLoading)
        addHook("prepareQA", self.onPrepareQA)

    def log(self, msg):
        mw.db.log(msg)

    def toggle(self, f):
        self.hookers[f][0] = not self.hookers[f][0]
        self.log("Logging "+self.hookers[f][1]+"="+('on' if self.hookers[f][0] else 'off'))

    def onUndoState(self, bool):
        if self.hookers['ALL'][0] or self.hookers['US'][0]:
            self.log('Hook:'+self.hookers['US'][1]+' bool='+str(bool))

    def onColLoading(self, col):
        if self.hookers['ALL'][0] or self.hookers['CL'][0]:
            self.log('Hook:'+self.hookers['CL'][1])

    def onBeforeStateChange(self, newS, oldS, *args):
        if self.hookers['ALL'][0] or self.hookers['BSC'][0]:
            self.log('Hook:'+self.hookers['BSC'][1]+' old=%s, new=%s'%(oldS,newS))

    def onAfterStateChange(self, newS, oldS, *args):
        if self.hookers['ALL'][0] or self.hookers['ASC'][0]:
            self.log('Hook:'+self.hookers['ASC'][1]+' old=%s, new=%s'%(oldS,newS))

    def onNoteChanged(self, id):
        if self.hookers['ALL'][0] or self.hookers['NC'][0]:
            self.log('Hook:'+self.hookers['NC'][1]+' id='+str(id))

    def onReset(self):
        if self.hookers['ALL'][0] or self.hookers['R'][0]:
            self.log('Hook:'+self.hookers['R'][1])

    def onShowQuestion(self):
        if self.hookers['ALL'][0] or self.hookers['Q'][0]:
            self.log('Hook:'+self.hookers['Q'][1])

    def onShowAnswer(self):
        if self.hookers['ALL'][0] or self.hookers['A'][0]:
            self.log('Hook:'+self.hookers['A'][1])

    def onProfileLoaded(self):
        if self.hookers['ALL'][0] or self.hookers['PL'][0]:
            self.log('Hook:'+self.hookers['PL'][1])

    def onUnloadProfile(self):
        if self.hookers['ALL'][0] or self.hookers['UP'][0]:
            self.log('Hook:'+self.hookers['UP'][1])

    def onPrepareQA(self, html, card, context): #v2.1
        if self.hookers['ALL'][0] or self.hookers['PQA'][0]:
            self.log('Hook:%s context="%s"'%(self.hookers['PQA'][1],context))


mw.db.hooks=HookTest()
