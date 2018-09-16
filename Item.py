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
        self.modifier = Props.Modifier()

        if 'Enhancement' in props:
            self.modifier.updateSource(('AttackBonus', 'Addtional', 'Enhancement'), int(props['Enhancement']))
            self.modifier.updateSource(('Damage', 'Addtional', 'Magical', 'Enhancement'), int(props['Enhancement']))

        self.props['Type'] = 'Weapon'
        protoName = self.props['BaseItem']
        if protoName in self.ctx['protosWeapon']:
            self.proto = self.ctx['protosWeapon'][protoName].proto
        else:
            # for a virtual weapon, we need following keys in |props|:
            #   BaseCriticalThreat, default is [20, 20, 2], also named as 20/x2
            #   BaseDamage, default is [1,4,1], also named as 1d4
            #   BaseDamageType, default is ['Bludgeoning']
            self.proto = {'BaseDamageType': ['Bludgeoning'], 'WeaponSize': 'Tiny', 'Weight': 0.0,
                          'BaseCriticalThreat': {'desc': '20-20/x2', 'params': [20, 20, 2]}}
            self.proto['name'] = 'Virtual:' + protoName
            self.proto['BaseDamage'] = {'desc': '1d4', 'params': [1, 4, 1]}
            if 'BaseDamage' in props:
                params = props['BaseDamage']
                if type(params) == list and len(params) == 3:
                    self.proto['BaseDamage']['params'] = params
                    self.proto['BaseDamage']['desc'] = '%dd%d'.format(params[2], params[1])
            if 'BaseDamageType' in props:
                self.proto['BaseDamageType'] = props['BaseDamageType']
            if 'BaseCriticalThreat' in props:
                params = props['BaseCriticalThreat']
                if type(params) == list and len(params) == 3:
                    self.proto['BaseCriticalThreat']['params'] = params
                    self.proto['BaseCriticalThreat']['desc'] = '%d-%d/x%d'.format(params[0], params[1], params[2])

        if 'name' not in self.props:
            # make weapon name if not provided
            nameWithEnhancement = self.proto['name']
            if 'Enhancement' in props:
                nameWithEnhancement += str(props['Enhancement'])
            self.props['name'] = nameWithEnhancement

        criticalParams = self.proto['BaseCriticalThreat']['params']
        self.modifier.updateSource(('CriticalRange', 'Base', self.props['name']), criticalParams[1] - criticalParams[0])
        self.modifier.updateSource(('CriticalMultiplier', 'Base', self.props['name']), criticalParams[2])

    def __str__(self):
        return self.props['name']

    def getAttackBonus(self, target):
        abAdditional = self.modifier.sumSource(('AttackBonus', 'Addtional'))
        # todo: ab from weapon's Buff(MagicWeapon etc.), VS alignment
        return abAdditional

    def getCriticalThreat(self):
        minMaxDiff = self.modifier.sumSource('CriticalRange')
        multiplierSources = self.modifier.getSource('CriticalMultiplier')
        return (minMaxDiff, multiplierSources)