#coding: utf-8
from Dice import rollDice
from Apply import *
from common import Props
import Damages

class BuffManager:
    def __init__(self, unit):
        self.owner = unit
        self.buffs = []
        self.tsInMs = 0

    def addBuff(self, buffCaster, buffProto, buffMetaMagics = []):
        expired = buffProto.calcDuration(buffCaster, buffMetaMagics) * 1000 + time.now
        if buffProto.name not in self.buffs:
            self.buffs.append([buffCaster, expired, buffProto, buffMetaMagics, False])
        else:
            buffExist = self.buffs[self.buffs.index(buffProto.name)]
            if buffExist[1] > expired:
                print('weak buff', buffProto.name, 'cast from', repr(buffCaster))
                return False

            buffExist = [buffCaster, expired, buffProto, buffMetaMagics, False]
        print('buff', buffProto.name, 'cast from', repr(buffCaster))
        return True

    def update(self, deltaTime):
        self.tsInMs += int(1000 * deltaTime)
        if len(self.buffs) == 0:
            return

        # remove expired buff, one per update call
        for i, buff in enumerate(self.buffs):
            if not buff[4]:
                buff[4] = True
                buff[2].applyModifier(buff[0], self.owner.modifierBuff, buff[3])
                print('buff', buff[2].name, 'applied for', repr(self.owner))

            if buff[1] <= self.tsInMs:
                self.buffs.pop(i)
                buff[2].removeModifier(self.owner.modifierBuff)
                print('buff', buff[2].name, 'expired, cast from', repr(buff[0]))
                break

