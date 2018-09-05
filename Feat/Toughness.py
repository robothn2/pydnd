#coding: utf-8

proto = {
    'name': 'Toughness',
    'Type': 'General',
    'Prerequisite': 'None',
    'Specifics': '''A character with this feat is tougher than normal, gaining one bonus hit point per level. Hit points are gained retroactively when choosing this feat.''',
    'Use': '''Automatic'''
}

def matchRequirements(unit):
    return True

def apply(unit):
    print('apply feat %s' % proto['name'])

    totalLevel = 0
    for cls in unit.getProp('classes').values():
        totalLevel += cls['level']

    unit.modifier.addTypedSource('HitPoint', proto['name'], totalLevel, 'Feat:' + proto['name'])

def check(caster, target):
    return True
