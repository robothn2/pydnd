#coding: utf-8

proto = {
    'name': 'GreatCharisma',
    'Type': 'Epic',
    'Prerequisite': 'Level 21.',
    'Use': '''Automatic'''
}
source = 'Feat:' + proto['name']

def matchRequirements(unit):
    return unit.getClassLevel() >= 21

def apply(unit, featParams):
    print('apply feat', proto['name'], ', params', featParams)

    unit.modifier.updateSource(('Abilities', 'Cha', 'Base', source), featParams[-1])
