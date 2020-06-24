#coding: utf-8

protos = {
  'name': 'Fighter',
  'type': 'Class',
  'desc': '''Of all the classes, the fighter has the best all around fighting capabilities (hence the name). Fighters are familiar with all the standard weapons and armors. In addition to general fighting prowess, each fighter develops particular specialties of his own. A given fighter may be especially capable with certain weapons; another might be trained to execute specific fancy maneuvers. As fighters gain experience, they get more opportunities to develop their fighting skills. Thanks to their focus on combat maneuvers, they can master the most difficult ones relatively quickly.''',
  'Hit Die': 'd10',
  'Base Attack Bonus': 'High',
  'High Saves': 'Fortitude.',
  'Weapon Proficiencies': ('Simple', 'Martial'),
  'Armor Proficiencies': ('Light', 'Medium', 'Heavy', 'Shield', 'TowerShield'),
  'Skill Points': 2,
  'Class Skills': ('CraftArmor', 'CraftWeapon', 'Intimidate', 'Parry', 'Taunt'),
  'bonus': (
    (1, ('FeatBonus', '''At 1st level, a fighter gets a bonus combat-oriented feat in addition to the feat that any 1st-level character gets and the bonus feat granted to a human character.''')),
    (lambda level: level % 2 == 0, ('FeatBonus', 'Combat', '''The fighter gains an additional bonus feat at 2nd level and every two fighter levels thereafter (4th, 6th, 8th, 10th, 12th, 14th, 16th, 18th, and 20th). These bonus feats must be drawn from the feats noted as fighter bonus feats. A fighter must still meet all prerequisites for a bonus feat, including ability score and base attack bonus minimums.''')),
  ),
}
