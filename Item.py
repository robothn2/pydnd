#coding: utf-8
from common import Props

class Item:
    def __init__(self, ctx, props):
        self.ctx = ctx
        self.props = Props.Props(props)
        self.modifier = Props.Modifier()

class Weapon(Item):
    def __init__(self, ctx, props):
        super(Weapon, self).__init__(ctx, props)
        self.props['Type'] = 'Weapon'
        protoName = self.props['BaseItem']
        self.proto = self.ctx['protosWeapon'][protoName].proto
