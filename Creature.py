#coding: utf-8

import Abilities
import Unit

class Creature(Unit.Unit):
    def __init__(self, ctx, name):
        super(Creature, self).__init__(ctx)
        proto = ctx['protosCreatures'][name]
        self.d = proto
        self.abilities = Abilities.Abilities([proto['Str'], proto['Dex'], proto['Con'],
                                    proto['Wis'], proto['Int'], proto['Cha']])
        self.level = proto['level']
        self.hp = proto['hp']
        self.ac = proto['ac']
        self.level = proto['level']
