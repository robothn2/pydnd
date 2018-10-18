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
    prop = unit.calc.getProp('Ability.Dex.Base')
    value = prop.calcSingleSource(source, unit, None)
    unit.calc.addSource('Ability.Dex.Base', name=source, calcInt=value+1)
