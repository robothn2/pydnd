#coding: utf-8
import Dice

proto = {
    'name': 'EpicProwess',
    'Type': 'General',
    'Prerequisite': 'Level 21',
    'Specifics': '''The character gains +1 attack bonus''',
    'Use': '''Automatic'''
}
source = 'Feat:' + proto['name']

def matchRequirements(unit):
    return unit.getClassLevel() >= 21

def apply(unit, featParams):
    unit.calc.addSource('AttackBonus.Additional', name=source, calcInt=1)
