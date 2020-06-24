#coding: utf-8

def __chargesTurnUndead(feat, unit):
    charge = 3 + unit.calc.calcPropValue('Modifier.Cha')
    if feat.hasMember('ExtraTurning'):
        charge += 4
    return charge

protos = [
  {
    'name': 'Turn Undead', 'group': 'TurnUndead',
    'type': 'Feat', 'category': 'Class',
    'charges': __chargesTurnUndead,
    'chargeSlot': 'TurnUndead',
    'specifics': '''With this feat, the character can force undead to cower in terror or destroy them outright. This ability may be activated three times per day, plus the cleric's Charisma modifier. Paladins are treated as clerics of three levels lower than their actual paladin level for purposes of turning undead, while blackguards are treated as clerics of two levels lower than their actual blackguard level.''',
  },
  {
    'name': 'Extra Turning', 'group': 'TurnUndead',
    'type': 'Feat', 'category': 'Class',
    'prerequisite': [('ClassAny', ('Cleric', 'Paladin'))],
    'specifics': '''This divine ability allows the character to turn undead four additional times per day.''',
  },

  {
    'name': 'Divine Might', 'group': 'DivineMight',
    'type': 'Feat', 'category': 'Class',
    'prerequisite': [('Feat', 'TurnUndead'), ('Feat', 'PowerAttack'), ('Ability', 'Cha', 13)],
    'chargeSlot': 'TurnUndead',
    'specifics': '''The character may spend one of his turn undead attempts to add his Charisma bonus to all weapon damage for a number of rounds equal to the Charisma bonus.''',
  },
  {
    'name': 'Epic Divine Might', 'group': 'DivineMight',
    'type': 'Feat', 'category': 'Epic',
    'prerequisite': [('Feat', 'DivineMight'), ('Level', 21), ('Ability', 'Str', 21), ('Ability', 'Cha', 21)],
    'specifics': '''When you use the Power Attack or Improved Power Attack feat with a one-handed weapon against a favored enemy, your Power Attack damage bonus is doubled. With a two-handed weapon against a favored enemy, your Power Attack damage bonus is tripled.''',
  },
]
