#coding: utf-8

proto = {
    'name': 'Toughness',
    'Type': 'General',
    'Prerequisite': 'None',
    'Specifics': '''A character with this feat is tougher than normal, gaining one bonus hit point per level. Hit points are gained retroactively when choosing this feat.''',
    'Use': '''Automatic'''
}
source = 'Feat:' + proto['name']

def matchRequirements(unit):
    return True

def apply(unit, featParams):
    unit.calc.addSource('HitPoint', name=source, calcInt=lambda caster,target: unit.getClassLevel())
