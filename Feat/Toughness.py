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

def apply(unit, featParams):
    print('apply feat %s' % proto['name'])

    totalLevel = unit.props.sumFieldValue('classes', 'level')
    unit.modifier.addTypedSource('HitPoint', proto['name'], totalLevel, 'Feat:' + proto['name'])

def applyAgainstTarget(caster, target):
    return True
