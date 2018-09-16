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

def condition(caster, weapon, params):
    #print('condition of', proto['name'], ': weapon', weapon.proto['name'], ', params', params)
    if not params or weapon.proto['name'] not in params:
        return

    if 'IncreasedMultiplier' in params:
        weapon.modifier.updateSource(('CriticalMultiplier', 'Additional', 'Feat:IncreasedMultiplier'), 1)
    if 'SuperiorWeaponFocus' in params:
        weapon.modifier.updateSource(('AttackBonus', 'Additional', 'Feat:SuperiorWeaponFocus'), 1)
    if 'KiCritical' in params:
        weapon.modifier.updateSource(('CriticalRange', 'Additional', 'Feat:KiCritical'), 2)

    #print('modifier for weapon', weapon.props['name'], weapon.modifier)

def apply(unit, featParams):
    print('apply feat %s' % proto['name'])
    unit.modifier.updateSource(('Conditional', 'Weapon', source), (condition, featParams))
