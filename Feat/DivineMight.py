#coding: utf-8
from Spell.Protos import SpellProtoBufferSelf

proto = {
    'name': 'DivineMight',
    'Type': 'General',
    'Prerequisite': 'Turn Undead, Cha 13+, Str 13+, Power Attack.',
    'Specifics': '''The character may spend one of his turn undead attempts to add his Charisma bonus to all weapon damage for a number of rounds equal to the Charisma bonus.''',
    'Use': '''Selected'''
}
source = proto['name']

def matchRequirements(unit):
    return unit.hasFeats(['TurnUndead', 'PowerAttack']) \
           and unit.calc.calcPropValue('Ability.Str') >= 13 \
           and unit.calc.calcPropValue('Ability.Cha') >= 13

def __buffDuration(caster, metaMagics):
    return 3600.0 * caster.getClassLevel()

def __buffApply(caster, propCalc, metaMagics):
    value = caster.calc.calcPropValue('Modifier.Cha', caster, None)
    propCalc.addSource('Damage.Additional', name=source, calcInt=lambda caster, target: ('Divine', source, value))

def __buffUnapply(propCalc):
    propCalc.removeSource('Damage.Additional', source)

def __castToTarget(caster, target, params):
    proto = caster.calc.getPropSource('Spell.Charges', source)
    caster.buffs.addBuff(caster, proto.calcInt)

def __fillCharge(caster):
    value = caster.calc.calcSingleSource('Spell.Charges', 'TurnUndead', caster, None)
    #caster.calc.addSource('Damage.Additional', name=source, calcInt=lambda caster,target: ('Physical', source, value))

def __decCharge(caster):
    pass

def apply(unit, featParams):
    spellProto = SpellProtoBufferSelf(source, params=featParams,
                                    castToTarget=__castToTarget, fillCharge=__fillCharge, decCharge=__decCharge,
                                    buffDuration=__buffDuration, buffApply=__buffApply, buffUnapply=__buffUnapply)
    unit.calc.addSource('Spell.Charges', name=source, calcInt=spellProto)
