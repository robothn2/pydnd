#coding: utf-8
from common import Props
from Dice import rollDice
import Apply

class Item:
    def __init__(self, ctx, props):
        self.ctx = ctx
        self.props = Props.Props(props)
        self.modifier = Props.Modifier()
    def getName(self):
        return self.props.get('name')

class Weapon(Item):
    def __init__(self, ctx, props):
        super().__init__(ctx, props)
        self.modifier = Props.Modifier()

        self.props['Type'] = 'Weapon'
        protoName = self.props['BaseItem']
        if protoName in self.ctx['protosWeapon']:
            self.proto = self.ctx['protosWeapon'][protoName].proto
        else:
            # for a natural weapon, we need following keys in |props|:
            #   BaseCriticalThreat, default is [20, 20, 2], also named as 20/x2
            #   BaseDamage, default is [1,4,1], also named as 1d4
            #   BaseDamageType, default is ['Bludgeoning']
            self.proto = {'BaseDamageType': ['Bludgeoning'], 'WeaponSize': 'Tiny', 'Weight': 0.0,
                          'BaseCriticalThreat': {'desc': '20-20/x2', 'params': [20, 20, 2]}}
            self.proto['name'] = 'NaturalWeapon:' + protoName
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
                nameWithEnhancement += '+' + str(props['Enhancement'])
            self.props['name'] = nameWithEnhancement

    def __str__(self):
        return self.props['name']
    def __repr__(self):
        return self.props['name']

    def getItemBaseName(self):
        return self.proto['name']

    def apply(self, unit, hand):
        Apply.apply_weapon_attacks(self, unit, hand)

        unit.calc.updateObject(('Weapon', hand), self)

        # weapon base damage
        weaponParams = self.proto['BaseDamage']['params']
        weaponName = self.props['name']
        unit.calc.addSource('Damage.' + hand, name=weaponName, calcInt=lambda caster, target: ('Physical', weaponName, rollDice(weaponParams[0], weaponParams[1], weaponParams[2])), noCache=True)

        # weapon enhancement
        enhanceValue = self.props.get('Enhancement')
        if enhanceValue != None:
            unit.calc.addSource('Weapon.%s.Additional' % hand, name='WeaponEnhancement', calcInt=('Magical', 'WeaponEnhancement', enhanceValue))
            unit.calc.addSource('AttackBonus.' + hand, name='WeaponEnhancement', calcInt=enhanceValue)

        # weapon critical parameter
        criticalParams = self.proto['BaseCriticalThreat']['params']
        unit.calc.addSource('Weapon.%s.CriticalRange' % hand, name='WeaponBase', calcInt=criticalParams[1] - criticalParams[0])
        unit.calc.addSource('Weapon.%s.CriticalMultiplier' % hand, name='WeaponBase', calcInt=criticalParams[2])

        # weapon related feats
        Apply.feats_apply_to_weapon(unit, self, hand)

    def unapply(self, unit, hand):
        unit.calc.removeSource('Attacks', hand)

        unit.calc.removeSource('Damage.' + hand, self.props['name'])

        unit.calc.removeSource('Weapon.%s.Additional' % hand, 'WeaponEnhancement')
        unit.calc.removeSource('Damage.' + hand, 'WeaponEnhancement')

        unit.calc.removeSource('Weapon.%s.CriticalRange' % hand, 'WeaponBase')
        unit.calc.removeSource('Weapon.%s.CriticalMultiplier' % hand, 'WeaponBase')

