#coding: utf-8

def _addDeityWeaponFocus(unit):
  deityName = unit.getProp('deity')
  deity = unit.ctx['Deity'].get(deityName)
  if not deity:
    return

  weapon = deity.favoredWeapon
  print('deity:', deityName, ', favored weapon:', weapon)
  if weapon == 'Unarmed Strike':
    unit.addFeat('Improved Unarmed Strike')
  else:
    unit.addFeat('Weapon Proficiency', weapon)
    unit.addFeat('Weapon Focus', weapon)

protos = [
  {
    'name': 'War',
    'type': 'Domain',
    'bonus': [
      (_addDeityWeaponFocus, '''The cleric receives the weapon focus feat for their deity's favored weapon. They are also proficient with that weapon even if clerics normally are not. If their deity's favored weapon is unarmed strike, they gain the improved unarmed strike feat.'''),
      ('SpellAccess', 'Cleric', ('Flame Strike', 'Power Word Stun')),
    ],
    'desc': '''Clerics who take the War domain spend considerable time training for combat.''',
  },
]
