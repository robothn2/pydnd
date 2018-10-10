#coding: utf-8
import Dice

proto = {
    'name': 'TurnUndead',
    'Type': 'Class',
    'Prerequisite': 'Cleric level 1, paladin level 4 or blackguard level 3.',
    'RequiredFor': 'Divine Might and Divine Shield.',
    'Specifics': '''With this feat, the character can force undead to cower in terror or destroy them outright. This ability may be activated three times per day, plus the cleric's Charisma modifier. Paladins are treated as clerics of three levels lower than their actual paladin level for purposes of turning undead, while blackguards are treated as clerics of two levels lower than their actual blackguard level.''',
    'Use': '''Selected'''
}
source = 'Feat:' + proto['name']

def matchRequirements(unit):
    return True

def castTo(caster, target):
    pass

def apply(unit, featParams):
    chargeSource = [0, # charges, can be initialized by init-function if unit take a rest
                    (lambda unit: 3 + unit.calc.calcPropValue('Modifier.Cha'))] # charges init-function,
    sourceParams = [chargeSource, castTo]
    unit.calc.addSource('Spell.Charges', name='TurnUndead', calcInt=sourceParams)
