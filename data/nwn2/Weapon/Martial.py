#coding: utf-8

protos = [
  {
    'name': 'Battleaxe',
    'type': 'Weapon', 'feat': 'Martial',
    'damageRoll': (1,8),       # 1d8
    'criticalThreat': (2,3),   # 19-20/x3
    'damageType': 'Slashing',
    'size': 'Medium',
    'weight': 6.0,
    'specifics': '''The battleaxe consists of a single blade atop a three- or four-foot shaft. It is a versatile weapon, and remains a useful tool when not in combat.''',
  },
  {
    'name': 'Falchion',
    'type': 'Weapon', 'feat': 'Martial',
    'damageRoll': (2,4),
    'criticalThreat': (4,2),
    'damageType': 'Slashing',
    'size': 'Large',
    'weight': 8.0,
    'specifics': '''This sword, which is essentially a two-handed scimitar, has a curve that gives it the effect of a keener edge.''',
  },
  {
    'name': 'Flail',
    'type': 'Weapon', 'feat': 'Martial',
    'damageRoll': (1,8),
    'criticalThreat': (2,2),
    'damageType': 'Bludgeoning',
    'size': 'Medium',
    'weight': 5.0,
    'specifics': '''Originally a farm implement for threshing grain, the flail consists of a wooden shaft attached to a heavy or spiked head by a chain or hinge. The flail is approximately two feet long.''',
  },
  {
    'name': 'Greataxe',
    'type': 'Weapon', 'feat': 'Martial',
    'damageRoll': (1,12),
    'criticalThreat': (2,3),
    'damageType': 'Slashing',
    'size': 'Large',
    'weight': 12.0,
    'specifics': '''A favorite of barbarians, the greataxe is the largest of the weapons derived from the basic woodcutter's axe. The double-edged head is far more suited to cleaving opponents than trees.''',
  },
  {
    'name': 'Greatsword',
    'type': 'Weapon', 'feat': 'Martial',
    'damageRoll': (2,6),
    'criticalThreat': (3,2),
    'damageType': ('Slashing','Piercing'),
    'size': 'Large',
    'weight': 8.0,
    'specifics': '''The greatsword is an impressive weapon by any measure, and is held with two hands by all but the largest of creatures.''',
  },
  {
    'name': 'Halberd',
    'type': 'Weapon', 'feat': 'Martial',
    'damageRoll': (1,10),
    'criticalThreat': (2,3),
    'damageType': ('Slashing','Piercing'),
    'size': 'Large',
    'weight': 12.0,
    'specifics': '''The halberd is the most common polearm, and could be called a cross between a spear and an axe. Such weapons are often mass-produced for militia, and serve well when defending against marauders.''',
  },
  {
    'name': 'Handaxe',
    'type': 'Weapon', 'feat': 'Martial',
    'damageRoll': (1,6),
    'criticalThreat': (2,3),
    'damageType': 'Slashing',
    'size': 'Small',
    'weight': 3.0,
    'specifics': '''The handaxe is smaller than most axes used for combat, and is most often used as an off-hand weapon.''',
  },
  {
    'name': 'Kukri',
    'type': 'Weapon', 'feat': 'Martial',
    'damageRoll': (1,4),
    'criticalThreat': (4,2),
    'damageType': 'Slashing',
    'size': 'Tiny',
    'weight': 2.0,
    'specifics': '''Kukri are heavy, curved daggers with their sharpened edge on the inside arc of the blade. This type of weapon has its roots as a tool, but has been heavily adapted to ritual and warfare.''',
  },
  {
    'name': 'Light Hammer',
    'type': 'Weapon', 'feat': 'Martial',
    'damageRoll': (1,4),
    'criticalThreat': (2,2),
    'damageType': 'Bludgeoning',
    'size': 'Small',
    'weight': 2.0,
    'specifics': '''The light hammer is derived from commonly used mining tools. It remains small enough to still be used in excavation, unlike the much heavier warhammer.''',
  },
  {
    'name': 'Longbow',
    'type': 'Weapon', 'feat': 'Martial',
    'damageRoll': (1,8),
    'criticalThreat': (2,3),
    'damageType': 'Piercing',
    'size': 'Large',
    'weight': 3.0,
    'specifics': '''The longbow is a refinement of the shortbow, designed to increase the range and power of an arrow strike. The stave portion of a longbow is nearly as tall as the archer, and can reach over six feet.''',
  },
  {
    'name': 'Longsword',
    'type': 'Weapon', 'feat': 'Martial',
    'damageRoll': (1,8),
    'criticalThreat': (3,2),
    'damageType': ('Slashing','Piercing'),
    'size': 'Medium',
    'weight': 4.0,
    'specifics': '''The longsword is the weapon most commonly associated with knights and their ilk. There are many variations in the blade, but all are approximately 35 to 47 inches in length.''',
  },
  {
    'name': 'Rapier',
    'type': 'Weapon', 'feat': 'Martial',
    'damageRoll': (1,6),
    'criticalThreat': (4,2),
    'damageType': 'Piercing',
    'size': 'Medium',
    'weight': 2.0,
    'specifics': '''The rapier is a light, thrusting sword popular among nobles and swashbucklers. Often associated with dueling and sport fighting, rapiers are nonetheless deadly in trained hands.''',
  },
  {
    'name': 'Scimitar',
    'type': 'Weapon', 'feat': 'Martial',
    'damageRoll': (1,6),
    'criticalThreat': (4,2),
    'damageType': 'Slashing',
    'size': 'Medium',
    'weight': 4.0,
    'specifics': '''The scimitar shares some similarities with the longsword and other slashing blades, but the severity and thickness of its curve clearly sets it apart.''',
  },
  {
    'name': 'Scythe',
    'type': 'Weapon', 'feat': 'Martial',
    'damageRoll': (2,4),
    'criticalThreat': (2,4),
    'damageType': ('Slashing','Piercing'),
    'size': 'Large',
    'weight': 10.0,
    'specifics': '''While obviously resembling the farm implement it is derived from, a scythe built for war is reinforced to withstand the rigors of combat.''',
  },
  {
    'name': 'Short Sword',
    'type': 'Weapon', 'feat': 'Martial',
    'damageRoll': (1,6),
    'criticalThreat': (3,2),
    'damageType': 'Piercing',
    'size': 'Small',
    'weight': 2.0,
    'specifics': '''One of the first types of sword to come into existence, the short sword is a double-edged weapon about two feet long. It is an economical weapon, and a favorite of archers and rogues.''',
  },
  {
    'name': 'Shortbow',
    'type': 'Weapon', 'feat': 'Martial',
    'damageRoll': (1,6),
    'criticalThreat': (2,3),
    'damageType': 'Piercing',
    'size': 'Medium',
    'weight': 2.0,
    'specifics': '''A shortbow has a stave portion of about five feet in length. The shortbow was the first of such launchers to be developed, and it remains an effective weapon.''',
  },
  {
    'name': 'Throwing Axe',
    'type': 'Weapon', 'feat': 'Martial',
    'damageRoll': (1,6),
    'criticalThreat': (2,2),
    'damageType': 'Slashing',
    'size': 'Tiny',
    'weight': 0.0,
    'specifics': '''The throwing axe bears little in common with the farm implement it is derived from. It has been carefully balanced for flight, sacrificing durability for precision.''',
  },
  {
    'name': 'Warhammer',
    'type': 'Weapon', 'feat': 'Martial',
    'damageRoll': (1,8),
    'criticalThreat': (2,3),
    'damageType': 'Bludgeoning',
    'size': 'Medium',
    'weight': 5.0,
    'specifics': '''Originally adapted from the tools of laborers and craftsmen, the warhammer is a far-heavier variant of the sledge and is no longer suitable for anything but combat.''',
  },
  {
    'name': 'Warmace',
    'type': 'Weapon', 'feat': 'Martial',
    'damageRoll': (1,12),
    'criticalThreat': (2,2),
    'damageType': 'Bludgeoning',
    'size': 'Large',
    'weight': 9.0,
    'specifics': '''Top-heavy and unwieldy the warmace is a larger variant of the common footman's mace that sacrifices elegance for effectiveness.''',
  },
]
