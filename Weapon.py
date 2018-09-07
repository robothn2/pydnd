#coding: utf-8
import warnings
from common import Props
from Item import Item

class Weapon(Item):
    def __init__(self, ctx, props):
        super(Weapon, self).__init__(ctx, props)
        self.props['Type'] = 'Weapon'
        protoName = self.props['BaseItem']
        self.proto = self.ctx['protosWeapon']

    def apply(self, unit):
        unit.modifier.updateUniqueSource(('MeleeDamage', 'Base'), self.proto['BaseDamage']['params'])