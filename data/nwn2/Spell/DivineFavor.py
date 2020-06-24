#coding: utf-8

def __buffApply(spell, caster, target, **kwargs):
    level = caster.calc.calcPropValue('Caster.Level', caster)
    value = max(1, min(3, int(level / 3)))
    target.calc.addSource('AttackBonus.Additional', name=spell.nameBuff, calcInt=value)
    target.calc.addSource('Damage.Additional', name=spell.nameBuff, calcInt=lambda caster,target: ('Magical', spell.nameBuff, value))

def __buffUnapply(spell, caster, target, **kwargs):
    target.calc.removeSource('AttackBonus.Additional', spell.nameBuff)
    target.calc.removeSource('Damage.Additional', spell.nameBuff)

protos = {
  'name': 'Divine Favor',
  'type': 'Spell',
  'InnateLevel': 1,
  'School': 'Evocation',
  'prerequisite': [('ClassLevel', 'Cleric', 1), ('ClassLevel', 'Paladin', 1)],
  'Component': ['Verbal', 'Somatic'],
  'Target': 'Caster',
  'Range': 'Personal',
  'Duration': '1 minute',
  'Save': [],
  'SpellResistance': False,
  'specifics': '''You gain a +1 bonus to attack and a +1 magical damage bonus for every three caster levels you have (minimum +1, maximum of +3).''',

  'buffDuration': 60,
  'buffApply': __buffApply,
  'buffUnapply': __buffUnapply,
}
