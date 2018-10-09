#coding: utf-8

proto = {
    'name': 'WeaponOfChoice',
    'Type': 'Class',
    'Prerequisite': 'Weapon Focus (with weapon to be chosen).',
    'Specifics': '''The weapon chosen to be a weapon of choice by a Weapon Master becomes the focus for all of their special abilities.''',
    'Use': '''Automatic'''
}
protoIncreasedMultiplier = {
    'name': 'IncreasedMultiplier',
    'Type': 'Class',
    'Prerequisite': 'Weapon of Choice, Weapon Master level 5.',
    'Specifics': '''With their weapon of choice, the multiplier is increased by x1 to all critical hits. Thus a x2 critical multiplier becomes a x3.''',
    'Use': '''Automatic'''
}
protoSuperiorWeaponFocus = {
    'name': 'SuperiorWeaponFocus',
    'Type': 'Class',
    'Prerequisite': 'Weapon of Choice, Weapon Master level 5.',
    'Specifics': '''The weapon master gains a +1 bonus to all attack rolls with their weapon of choice.''',
    'Use': '''Automatic'''
}
protoKiCritical = {
    'name': 'KiCritical',
    'Type': 'Class',
    'Prerequisite': 'Weapon of Choice, Weapon Master level 7.',
    'Specifics': '''The weapon master gains an additional +2 to the threat range of their weapon of choice.''',
    'Use': '''Automatic'''
}
source = 'Feat:' + proto['name']

def applyToWeapon(unit, featParams, weapon, hand):
    if type(featParams) != list or weapon.proto['name'] not in featParams:
        return

    print(source, 'affects weapon:', weapon.proto['name'], ', params:', featParams)
    if 'IncreasedMultiplier' in featParams:
        unit.calc.addSource('Weapon.%s.CriticalMultiplier' % hand, name='Feat:IncreasedMultiplier', calcInt=1)
    if 'SuperiorWeaponFocus' in featParams:
        unit.calc.addSource('AttackBonus.' + hand, name='Feat:SuperiorWeaponFocus', calcInt=1)
    if 'KiCritical' in featParams:
        unit.calc.addSource('Weapon.%s.CriticalRange' % hand, name='Feat:KiCritical', calcInt=2)
