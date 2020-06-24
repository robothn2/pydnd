#coding: utf-8

protos = [
  {
    'name': 'Bastard Sword',
    'type': 'Weapon', 'feat': 'Martial',
    'damageRoll': (1,10),       # 1d10
    'criticalThreat': (3,2),   # 18-20/x2
    'damageType': ('Slashing', 'Piercing'),
    'size': 'Medium',
    'weight': 6.0,
    'specifics': '''Bastard swords are also known as hand-and-a-half swords, falling between the longsword and greatsword in length.''',
  },
  {
    'name': 'Dwarven Waraxe',
    'type': 'Weapon', 'feat': 'Martial',
    'damageRoll': (1,10),
    'criticalThreat': (2,3),
    'damageType': 'Slashing',
    'size': 'Medium',
    'weight': 8.0,
    'specifics': '''A dwarven waraxe is much like the dwarves themselves; strong, hardy and very brutal.''',
  },
  {
    'name': 'Kama',
    'type': 'Weapon', 'feat': 'Martial',
    'damageRoll': (1,6),
    'criticalThreat': (2,2),
    'damageType': 'Slashing',
    'size': 'Small',
    'weight': 2.0,
    'specifics': '''As with many weapons, the kama was adapted for combat by the peasants that used them as farming implements, often because they were forbidden from owning swords or the like.''',
  },
  {
    'name': 'Katana',
    'type': 'Weapon', 'feat': 'Martial',
    'damageRoll': (1,10),
    'criticalThreat': (3,2),
    'damageType': ('Slashing', 'Piercing'),
    'size': 'Medium',
    'weight': 5.0,
    'specifics': '''The katana is the pinnacle of the swordsmith's craft, combining grace and artful design with razor-edged efficiency.''',
  },
  {
    'name': 'Shuriken',
    'type': 'Weapon', 'feat': 'Martial',
    'damageRoll': (1,3),
    'criticalThreat': (2,2),
    'damageType': 'Piercing',
    'size': 'Tiny',
    'weight': 0.0,
    'specifics': '''Shuriken are light, easy to conceal, and while they do little damage individually, they can be thrown very quickly.''',
  },
]
