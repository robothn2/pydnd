#coding: utf-8

proto = {
    'name': 'FavoredEnemy',
    'Type': 'Class',
    'Prerequisite': 'Ranger level 1.',
    'Specifics': '''The character gains a +1 bonus to damage rolls against their favored enemy. They also receive a +1 bonus on Listen, Spot, and Taunt checks against the favored enemy. Every 5 levels, the ranger may choose an additional Favored Enemy and all bonuses against all favored enemies increase by +1.''',
    'Use': '''Automatic'''
}

def matchRequirements(unit):
    return True

def apply(unit, featParams):
    print('apply feat', proto['name'], ', params', featParams)

    rangerLevel = unit.props['classes']['Ranger']['level']
    bonus = int(rangerLevel / 5)
    if bonus == 0:
        bonus = 1
    for _, raceName in enumerate(featParams):
        unit.modifier.updateSource(('MeleeDamage', 'Additional', 'Racial', 'Feat:' + proto['name']), bonus)
        unit.modifier.updateSource(('RangeDamage', 'Additional', 'Racial', 'Feat:' + proto['name']), bonus)

def applyAgainstTarget(caster, target):
    return True
