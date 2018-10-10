#coding: utf-8

proto = {
    'name': 'GreatDexterity',
    'Type': 'Epic',
    'Prerequisite': 'Level 21.',
    'Use': '''Automatic'''
}
source = 'Feat:' + proto['name']

def matchRequirements(unit):
    return unit.getClassLevel() >= 21

def apply(unit, featParams):
    unit.modifier.updateSource(('Abilities', 'Dex', 'Base', source), featParams[-1])
