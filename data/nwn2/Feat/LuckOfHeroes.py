#coding: utf-8

proto = {
    'name': 'LuckOfHeroes',
    'Type': 'Background',
    'Prerequisite': 'Can only take this feat at 1st-level, Cleric Domain: Luck, or Swashbuckler level 11.',
    'Specifics': '''Character gains a +1 bonus on all saving throws as well as a +1 luck bonus to Armor Class.''',
    'Use': '''Automatic'''
}
source = 'Feat:' + proto['name']

def matchRequirements(unit):
    return True

def apply(unit, featParams):
    unit.calc.addSource('SavingThrow.All', name=source, calcInt=1)
    unit.calc.addSource('ArmorClass.Luck', name=source, calcInt=1)
