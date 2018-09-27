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
        expired = int(1000 * (buffProto.calcDuration(buffCaster, buffMetaMagics))) + self.tsInMs
        buffName = buffProto.proto['name']
        if buffName not in self.buffs:
            self.buffs.append([buffCaster, expired, buffProto, buffMetaMagics])
        else:
            buffExist = self.buffs[self.buffs.index(buffName)]
            if buffExist[1] > expired:
                print('weak buff', buffName, 'cast from', repr(buffCaster))
                return False

            buffExist = [buffCaster, expired, buffProto, buffMetaMagics]

        # apply buff to owner
        buffProto.applyModifier(buffCaster, self.owner.modifierBuff, buffMetaMagics)
        print(repr(self.owner), 'applied buff', buffProto.proto['name'], ', cast from', repr(buffCaster))
        return True

    def update(self, deltaTime):
        self.tsInMs += int(1000 * deltaTime)
        if len(self.buffs) == 0:
            return

        # remove expired buff, one per update call
        for i, buff in enumerate(self.buffs):
            if buff[1] <= self.tsInMs:
                self.buffs.pop(i)
                buff[2].removeModifier(self.owner.modifierBuff)
                print('buff', buff[2].proto['name'], 'expired, cast from', repr(buff[0]))
                break

