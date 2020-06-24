#coding: utf-8


def __active(feat, caster, target, **kwargs):
  value = 6 if feat.hasMember('Improved') else 3
  caster.calc.addSource('AttackBonus.Additional', name=feat.nameFull, calcInt=-value)
  caster.calc.addSource('Damage.Additional', name=feat.nameFull, calcInt=lambda caster, target: ('Physical', feat.nameFull, value))
  if feat.hasMember('Favored'):
    caster.calc.addSource('Damage.TwoHand', name='Favored Power Attack', calcInt=lambda caster, target: ('Physical', 'Favored Power Attack', value*2))
    caster.calc.addSource('Damage.MainHand', name='Favored Power Attack', calcInt=lambda caster, target: ('Physical', 'Favored Power Attack', value))
    caster.calc.addSource('Damage.OffHand', name='Favored Power Attack', calcInt=lambda caster, target: ('Physical', 'Favored Power Attack', value))

def __deactive(feat, caster):
  caster.calc.removeSource('AttackBonus.Additional', feat.nameFull)
  caster.calc.removeSource('Damage.Additional', feat.nameFull)
  if feat.hasMember('Favored'):
    caster.calc.removeSource('Damage.TwoHand', 'Favored Power Attack')
    caster.calc.removeSource('Damage.MainHand', 'Favored Power Attack')
    caster.calc.removeSource('Damage.OffHand', 'Favored Power Attack')

protos = [
  {
    'name': 'Power Attack', 'group': 'PowerAttack',
    'type': 'Feat', 'catgory': 'General',
    'apply': __active,
    'unapply': __deactive,
    'prerequisite': [('Ability', 'Str', 13)],
    'specifics': '''A character with this feat can make powerful but ungainly attacks. When Power Attack is selected, it grants a +3 bonus to the damage roll, but at the cost of -3 to the attack roll.''',
  },

  {
    'name': 'Improved Power Attack', 'group': 'PowerAttack',
    'type': 'Feat', 'catgory': 'General',
    'prerequisite': [('Feat', 'PowerAttack'), ('BaseAttackBonus', 6)],
    'specifics': '''This feat allows the character to trade a -6 penalty on his attack roll to gain a +6 bonus on his damage roll. It is very useful when fighting tough, easy-to-hit opponents.''',
  },

  {
    'name': 'Favored Power Attack', 'group': 'PowerAttack',
    'type': 'Feat', 'catgory': 'Ranger',
    'prerequisite': [('Feat', 'FavoredEnemy'), ('Feat', 'PowerAttack'), ('BaseAttackBonus', 4)],
    'specifics': '''When you use the Power Attack or Improved Power Attack feat with a one-handed weapon against a favored enemy, your Power Attack damage bonus is doubled. With a two-handed weapon against a favored enemy, your Power Attack damage bonus is tripled.''',
  },
]
