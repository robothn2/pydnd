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
    prop = unit.calc.getProp('Ability.Cha.Base')
    value = prop.calcSingleSource(source, unit, None)
    unit.calc.addSource('Ability.Cha.Base', name=source, calcInt=value+1)
