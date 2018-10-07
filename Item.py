#coding: utf-8
from common import Props
from Dice import rollDice

def calc_attackbonus_list(maxAttackTimes, baseAttackBonus, babDecValue):
    bab = int(baseAttackBonus)
    abList = []
    while maxAttackTimes > 0:
        maxAttackTimes -= 1
        abList.append(bab)
        bab -= babDecValue
        if bab <= 0:
            break
    return abList

def calc_attacks_in_turn(maxAttackTimes, baseAttackBonus, babDecValue, secondsPerTurn, delaySecondsToFirstAttack,
                         weapon, hand):
    if maxAttackTimes == 0:
        return []
    babList = calc_attackbonus_list(maxAttackTimes, baseAttackBonus, babDecValue)
    durationAttack = (secondsPerTurn - delaySecondsToFirstAttack) / len(babList)
    tsOffset = delaySecondsToFirstAttack
    attacks = []
    for _,bab in enumerate(babList):
        attacks.append((round(tsOffset,3), bab, hand, weapon))
        tsOffset += durationAttack
    return attacks

class Item:
    def __init__(self, ctx, props):
        self.ctx = ctx
        self.props = Props.Props(props)
        self.modifier = Props.Modifier()
    def getName(self):
        return self.props.get('name')

class Weapon(Item):
    def __init__(self, ctx, props):
        super(Weapon, self).__init__(ctx, props)
        self.modifier = Props.Modifier()

        if 'Enhancement' in props:
            'Weapon.MainHand.Additional'
            self.modifier.updateSource(('AttackBonus', 'Additional', 'Enhancement'), int(props['Enhancement']))
            self.modifier.updateSource(('Damage', 'Additional', 'Magical', 'WeaponEnhancement'), int(props['Enhancement']))

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
                nameWithEnhancement += '+' + str(props['Enhancement'])
            self.props['name'] = nameWithEnhancement

        criticalParams = self.proto['BaseCriticalThreat']['params']
        self.modifier.updateSource(('CriticalRange', 'Base', self.props['name']), criticalParams[1] - criticalParams[0])
        self.modifier.updateSource(('CriticalMultiplier', 'Base', self.props['name']), criticalParams[2])

    def __str__(self):
        return self.props['name']
    def __repr__(self):
        return self.props['name']

    def getCriticalThreat(self):
        minMaxDiff = self.modifier.sumSource('CriticalRange')
        multiplierSources = self.modifier.getSource('CriticalMultiplier')
        return (minMaxDiff, multiplierSources)

    def apply(self, unit, hand):
        tsOffset = 0.5 if hand == 'OffHand' else 0.0
        bab = unit.calc.getPropValue('AttackBonus.Base', self, None)
        babDec = 5
        maxAttackTimes = 10
        if self.proto['name'] == 'Kama' and unit.getClassLevel('Monk') > 0:
            babDec = 3
        if hand == 'OffHand':
            if not unit.hasFeat('TwoWeaponFighting'):
                maxAttackTimes = 0
            else:
                featParams = unit.getFeatParams('TwoWeaponFighting')
                if 'Perfect' in featParams:
                    maxAttackTimes = 10
                elif 'Improved' in featParams:
                    maxAttackTimes = 2
                else:
                    maxAttackTimes = 1

        # attacks
        unit.calc.addSource('Attacks', name=hand, calcInt=lambda caster, target: \
            calc_attacks_in_turn(maxAttackTimes, bab, babDec, unit.ctx['secondsPerTurn'], tsOffset, self, hand))

        unit.calc.updateObject(('Weapon', hand), self)

        # weapon base damage
        weaponParams = self.proto['BaseDamage']['params']
        weaponName = self.props['name']
        unit.calc.addSource('Damage.' + hand, name=weaponName, calcInt=lambda caster, target: ('Physical', weaponName, rollDice(weaponParams[0], weaponParams[1], weaponParams[2])), noCache=True)
