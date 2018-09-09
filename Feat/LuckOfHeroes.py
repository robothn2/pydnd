#coding: utf-8

proto = {
    'name': 'LuckOfHeroes',
    'Type': 'Background',
    'Prerequisite': 'Can only take this feat at 1st-level, Cleric Domain: Luck, or Swashbuckler level 11.',
    'Specifics': '''Character gains a +1 bonus on all saving throws as well as a +1 luck bonus to Armor Class.''',
    'Use': '''Automatic'''
}

def matchRequirements(unit):
    return True

def apply(unit, featParams):
    print('apply feat %s' % proto['name'])

    unit.modifier.updateSource(('SavingThrow', 'All', 'Feat:' + proto['name']), 1)
    unit.modifier.updateSource(('ArmorClass', 'Luck', 'Feat:' + proto['name']), 1)

def applyAgainstTarget(caster, target):
    return True
