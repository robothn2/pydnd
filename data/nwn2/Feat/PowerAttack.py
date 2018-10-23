#coding: utf-8
from Feat.Protos import FeatProtoActivable

proto = {
    'name': 'PowerAttack',
    'Type': 'General',
    'Prerequisite': 'Turn Undead, Cha 13+, Str 13+, Power Attack.',
    'Specifics': '''The character may spend one of his turn undead attempts to add his Charisma bonus to all weapon damage for a number of rounds equal to the Charisma bonus.''',
    'Use': '''Selected'''
}
source = proto['name']

def matchRequirements(unit):
    return unit.calc.calcPropValue('Ability.Str') >= 13

def __active(caster, params):
    value = 10 if 'Improved' in params else 5
    caster.calc.addSource('AttackBonus.Additional', name=source, calcInt=-value)
    caster.calc.addSource('Damage.Additional', name=source, calcInt=lambda caster,target: ('Physical', source, value))

def __deactive(caster):
    caster.calc.removeSource('AttackBonus.Additional', source)
    caster.calc.removeSource('Damage.Additional', source)

def apply(unit, featParams):
    activator = FeatProtoActivable(active=__active, deactive=__deactive, params=featParams)
    unit.calc.addSource('Spell.Activable', name=source, calcInt=activator)
    print(unit.calc.getPropSource('Spell.Activable', source))