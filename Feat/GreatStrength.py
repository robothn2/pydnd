#coding: utf-8

proto = {
    'name': 'GreatStrength',
    'Type': 'Epic',
    'Prerequisite': 'Level 21.',
    'Use': '''Automatic'''
}
source = 'Feat:' + proto['name']

def matchRequirements(unit):
    return unit.getClassLevel() >= 21

def apply(unit, featParams):
    unit.modifier.updateSource(('Abilities', 'Str', 'Base', source), featParams[-1])
