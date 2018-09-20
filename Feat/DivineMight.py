#coding: utf-8
import Dice

proto = {
    'name': 'DivineMight',
    'Type': 'General',
    'Prerequisite': 'Turn Undead, Cha 13+, Str 13+, Power Attack.',
    'Specifics': '''The character may spend one of his turn undead attempts to add his Charisma bonus to all weapon damage for a number of rounds equal to the Charisma bonus.''',
    'Use': '''Selected'''
}
source = 'Feat:' + proto['name']

def matchRequirements(unit):
    return unit.getClassLevel() >= 21

def buffEffect(caster, target):
    value = caster.getAbilityModifier('Cha')
    caster.modifier.updateSource(('Conditional', 'Weapon', 'DivineMight'), value)

def castToTarget(caster, target):
    value = caster.getAbilityModifier('Cha')
    caster.addBuff(proto['name'], source, buffEffect, value * caster.ctx['secondsPerRound'])

def apply(unit, featParams):
    print('apply feat', proto['name'], ', params', featParams)
    sourceParams = unit.modifier.getSource(('Spell', 'Charges', 'TurnUndead'))
    chargeSource = sourceParams[0]
    unit.modifier.updateSource(('Spell', 'Charges', 'DivineMight'), [chargeSource, castToTarget])
