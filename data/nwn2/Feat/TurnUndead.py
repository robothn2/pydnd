#coding: utf-8
from Models import Feat, register_feat

def __castTurnUndead(spell, caster, target, **kwargs):
    pass
def __maxChargeTurnUndead(spell, caster, target, **kwargs):
    charge = 3 + caster.calc.calcPropValue('Modifier.Cha')
    params = kwargs.get('params')
    if params and 'ExtraTurning' in params:
        charge += 4
    return charge
def __decChargeTurnUndead(spell, caster, target, **kwargs):
    pass

def __spellCastDivineMight(spell, caster, target, **kwargs):
    target.buffs.addBuff(caster, spell, **kwargs)
def __buffDurationDivineMight(caster, **kwargs):
    turns = caster.calc.calcPropValue('Modifier.Cha', caster)
    #print('Divine might params:', kwargs)
    params = kwargs.get('params')
    if params and 'Epic' in params:
        turns *= 2
    return turns * caster.ctx['secondsPerTurn']
def __buffApplyDivineMight(spell, caster, target, **kwargs):
    value = caster.calc.calcPropValue('Modifier.Cha', caster)
    params = kwargs.get('params')
    print('Divine might params:', kwargs)
    if params and 'Epic' in params:
        value *= 2
    target.calc.addSource('Damage.Additional', name=spell.nameBuff, calcInt=lambda caster, target: ('Divine', spell.nameBuff, value))

def register(protos):
    # TurnUndead group
    register_feat(protos, 'TurnUndead', 'Turn Undead',
                  type='Class',
                  apply=lambda spell, caster, target, **kwargs: caster.calc.addSource('Spell.Charges', name=spell.nameFull, calcInt=spell),
                  unapply=lambda spell, caster, target, **kwargs: caster.calc.removeSource('Spell.Charges', spell.nameFull),
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
                  apply=lambda spell, caster, target, **kwargs: caster.calc.addSource('Spell.Charges', name=spell.nameFull, calcInt=spell),
                  unapply=lambda spell, caster, target, **kwargs: caster.calc.removeSource('Spell.Charges', spell.nameFull),
                  cast=__spellCastDivineMight,
                  maxCharge=__maxChargeTurnUndead,
                  decCharge=__decChargeTurnUndead,
                  buffDuration=__buffDurationDivineMight,
                  buffApply=__buffApplyDivineMight,
                  buffUnapply=lambda spell, caster, target, **kwargs: target.calc.removeSource('Damage.Additional', spell.nameBuff),
                  specifics='''The character may spend one of his turn undead attempts to add his Charisma bonus to all weapon damage for a number of rounds equal to the Charisma bonus.''',
                  )
    register_feat(protos, 'DivineMight', 'Epic Divine Might',
                  nameMember='Epic',
                  prerequisite=[('Feat', 'DivineMight'), ('Level', 21), ('Ability', 'Str', 21), ('Ability', 'Cha', 21)],
                  specifics='''When you use the Power Attack or Improved Power Attack feat with a one-handed weapon against a favored enemy, your Power Attack damage bonus is doubled. With a two-handed weapon against a favored enemy, your Power Attack damage bonus is tripled.''',
                  )
