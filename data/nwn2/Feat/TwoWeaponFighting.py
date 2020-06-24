#coding: utf-8

def _applyTwoWeaponFighting(feat, caster, target, **kwargs):
  weapon = kwargs.get('weapon')
  hand = kwargs.get('hand')
  params = kwargs.get('params')
  if hand == 'TwoHand':
    return
  if hand == 'OffHand':
    weaponMH = caster.calc.getObject(('Weapon', 'MainHand'))
    if weaponMH:
      caster.calc.addSource('AttackBonus.MainHand', name='Feat:TwoWeaponFighting', calcInt=-4)
      caster.calc.addSource('AttackBonus.OffHand', name='Feat:TwoWeaponFighting', calcInt=-4)
      if weapon.proto['WeaponSize'] in ['Tiny', 'Small']:
        caster.calc.addSource('AttackBonus.MainHand', name='Feat:TwoWeaponFighting', calcInt=2)
        caster.calc.addSource('AttackBonus.OffHand', name='Feat:TwoWeaponFighting', calcInt=2)
      # todo:
      if 'Perfect' in params:
        apply_weapon_attacks(weapon, caster, hand, 10)
      elif 'Greater' in params:
        apply_weapon_attacks(weapon, caster, hand, 3)
      elif 'Improved' in params:
        apply_weapon_attacks(weapon, caster, hand, 2)
      else:
        apply_weapon_attacks(weapon, caster, hand, 1)

protos = [
  {
    'name': 'Two-Weapon Fighting', 'group': 'TwoWeaponFighting',
    'type': 'Feat', 'catgory': 'Combat',
    'forWeapon': True,
    'prerequisite': [('Ability', 'Dex', 15)],
    'apply': _applyTwoWeaponFighting,
    'specifics': '''A character with this feat reduces the penalties suffered when fighting with two weapons. The normal penalty of -6 to the primary hand and -10 to the off-hand becomes -4 for the primary hand and -4 for the off-hand. Best results are achieved if the off-hand weapon is light, further reducing the penalty for both the primary and off-hand by 2 (to -2/-2).''',
  },
  {
    'name': 'Improved Two-Weapon Fighting', 'group': 'TwoWeaponFighting',
    'type': 'Feat', 'catgory': 'Combat',
    'prerequisite': [('Feat', 'Two-Weapon Fighting'), ('Ability', 'Dex', 17), ('BaseAttackBonus', 6)],
    'apply': _applyTwoWeaponFighting,
    'specifics': '''The character with this feat is able to get a second off-hand attack (at a penalty of -5 to his attack roll).''',
  },
  {
    'name': 'Greater Two-Weapon Fighting', 'group': 'TwoWeaponFighting',
    'type': 'Feat', 'catgory': 'Combat',
    'prerequisite': [('Feat', 'Improved Two-Weapon Fighting'), ('Ability', 'Dex', 19), ('BaseAttackBonus', 11)],
    'apply': _applyTwoWeaponFighting,
    'specifics': '''This feat grants a third attack with your off-hand weapon with a -10 attack penalty.''',
  },
  {
    'name': 'Perfect Two-Weapon Fighting', 'group': 'TwoWeaponFighting',
    'type': 'Feat', 'catgory': 'Epic',
    'prerequisite': [('Feat', 'Greater Two-Weapon Fighting'), ('Ability', 'Dex', 25), ('Level', 21)],
    'apply': _applyTwoWeaponFighting,
    'specifics': '''The character can make as many attacks with their off hand weapon as with their main hand weapon, using the same base attack bonus.''',
  },
]
