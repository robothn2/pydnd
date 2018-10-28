#coding: utf-8
from Models import Feat, register_feat

def __castTurnUndead(source, caster, feat, params):
    pass
def __maxChargeTurnUndead(source, unit, feat, params):
    charge = 3 + unit.calc.calcPropValue('Modifier.Cha')
    if 'ExtraTurning' in params:
        charge += 4
    return charge
def __decChargeTurnUndead(source, unit, feat, params):
    pass

def __buffDurationDivineMight(caster, feat, params):
    turns = caster.calc.calcPropValue('Modifier.Cha', caster)
    if 'Epic' in params:
        turns *= 2
    return turns * caster.ctx['secondsPerTurn']
def __buffApplyDivineMight(source, caster, target, feat, params):
    value = caster.calc.calcPropValue('Modifier.Cha', caster, None)
    if 'Epic' in params:
        value *= 2
    target.calc.addSource('Damage.Additional', name=source, calcInt=lambda caster, target: ('Divine', source, value))

def register(protos):
    # TurnUndead group
    register_feat(protos, 'TurnUndead', 'Turn Undead',
                  type='Class',
                  apply=lambda source, unit, feat, params: unit.calc.addSource('Spell.Charges', name=source, calcInt=feat),
                  unapply=lambda source, unit, feat, params: unit.calc.removeSource('Spell.Charges', source),
                  maxCharge=__maxChargeTurnUndead,
                  decCharge=__decChargeTurnUndead,
                  cast=__castTurnUndead,
                  prerequisite=[],
                  specifics='''With this feat, the character can force undead to cower in terror or destroy them outright. This ability may be activated three times per day, plus the cleric's Charisma modifier. Paladins are treated as clerics of three levels lower than their actual paladin level for purposes of turning undead, while blackguards are treated as clerics of two levels lower than their actual blackguard level.''',
                  )
    register_feat(protos, 'TurnUndead', 'Extra Turning',
                  type='Special',
                  prerequisite=[('ClassAny', ('Cleric', 'Paladin'))],
                  specifics='''This divine ability allows the character to turn undead four additional times per day.''',
                  )

    # DivineMight group
    register_feat(protos, 'DivineMight', 'Divine Might',
                  prerequisite=[('Feat', 'TurnUndead'), ('Feat', 'PowerAttack'), ('Ability', 'Str', 13), ('Ability', 'Cha', 13)],
                  apply=lambda source, unit, feat, params: unit.calc.addSource('Spell.Charges', name=source, calcInt=feat),
                  unapply=lambda source, unit, feat, params: unit.calc.removeSource('Spell.Charges', source),
                  maxCharge=__maxChargeTurnUndead,
                  decCharge=__decChargeTurnUndead,
                  buffApply=lambda source, caster, target: target.calc.removeSource('Damage.Additional', source),
                  buffUnapply=lambda source, caster, target: target.calc.removeSource('Damage.Additional', source),
                  cast=lambda caster, target, feat, params: target.buffs.addBuff(caster, feat),
                  specifics='''The character may spend one of his turn undead attempts to add his Charisma bonus to all weapon damage for a number of rounds equal to the Charisma bonus.''',
                  )
    register_feat(protos, 'DivineMight', 'Epic Divine Might',
                  prerequisite=[('Feat', 'DivineMight'), ('Level', 21), ('Ability', 'Str', 21), ('Ability', 'Cha', 21)],
                  specifics='''When you use the Power Attack or Improved Power Attack feat with a one-handed weapon against a favored enemy, your Power Attack damage bonus is doubled. With a two-handed weapon against a favored enemy, your Power Attack damage bonus is tripled.''',
                  )
