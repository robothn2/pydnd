#coding: utf-8

def availableParams(unit):
    if not unit.hasFeat('Weapon Proficiency'):
        return []

    weapons = unit.getFeatParams('Weapon Proficiency')
    race = unit.getProp('race')
    if race not in ['Gnomes', 'Halflings']:
        return weapons

    # Halflings and gnomes cant use large weapons
    weaponsAvailable = []
    for _, weaponBaseName in weapons:
        weaponProto = unit.ctx['Weapon'][weaponBaseName]
        if weaponProto.proto['WeaponSize'] != 'Large':
            weaponsAvailable.append(weaponBaseName)
    return weaponsAvailable

def __applyWeaponFocus(feat, caster, target, **kwargs):
    weapon = kwargs.get('weapon')
    hand = kwargs.get('hand')
    params = kwargs.get('params')
    if type(params) is not list or weapon.nameBase not in params:
        return

    print(feat.nameFull, 'affects weapon:', weapon.getItemBaseName(), ', params:', params)
    caster.calc.addSource('AttackBonus.' + hand, name='WeaponFocus', calcInt=1)
    if 'Greater' in params:
        caster.calc.addSource('AttackBonus.' + hand, name='GreaterWeaponFocus', calcInt=1)
    if 'Epic' in params:
        caster.calc.addSource('AttackBonus.' + hand, name='EpicWeaponFocus', calcInt=2)
    if 'ImprovedCritical' in params:
        criticalParams = weapon.proto['BaseCriticalThreat']['params']
        rangeDiff = criticalParams[1] - criticalParams[0]
        caster.calc.addSource('Weapon.%s.CriticalRange' % hand, name=feat.nameFull, calcInt=rangeDiff)
def __unapplyWeaponFocus(feat, caster, target, **kwargs):
    caster.calc.removeSource('AttackBonus.TwoHand', feat.nameMember)
    caster.calc.removeSource('AttackBonus.MainHand', feat.nameMember)
    caster.calc.removeSource('AttackBonus.OffHand', feat.nameMember)


protos = [
  {
    'name': 'Weapon Focus', 'group': 'WeaponFocus',
    'type': 'Feat', 'catgory': 'Combat',
    'forWeapon': True,
    'prerequisite': [('BaseAttackBonus', 1), ('Feat', 'Weapon Proficiency')],
    'apply': __applyWeaponFocus,
    'unapply': __unapplyWeaponFocus,
    'specifics': '''A character with this feat is particularly skilled with a specific weapon, gaining a +1 attack bonus with it.''',
  },
  {
    'name': 'Greater Weapon Focus', 'group': 'WeaponFocus',
    'type': 'Feat', 'catgory': 'Combat',
    'prerequisite': [('ClassLevel', 'Fighter', 8), ('Feat', 'Weapon Focus')],
    'specifics': '''This feat grants an additional +1 to hit bonus with the selected weapon. This stacks with all other bonuses to attack roll (including Weapon Focus). This feat can be taken multiple times, but each time the effect applies to a new type of weapon.''',
  },
  {
    'name': 'Epic Weapon Focus', 'group': 'WeaponFocus',
    'type': 'Feat', 'catgory': 'Epic',
    'prerequisite': [('Level', 21), ('Feat', 'Greater Weapon Focus')],
    'specifics': '''The character gains +4 bonus to all attack rolls made using the selected weapon. This feat can be taken multiple times, but it applies to a different weapon each time. This bonus replaces that of Weapon Focus and Greater Weapon Focus.''',
  },
  {
    'name': 'Improved Critical', 'group': 'WeaponFocus',
    'type': 'Feat', 'catgory': 'Epic',
    'prerequisite': [('Feat', 'Weapon Focus'), ('BaseAttackBonus', 4)],
    'specifics': '''Combat ability doubles the critical threat range with a given weapon. A longsword that normally threatens a critical on a roll of 19-20 would now threaten a critical on a roll of 17-20.''',
  },
]
