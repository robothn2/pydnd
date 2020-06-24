#coding: utf-8

protos = {
  'name': 'Monk',
  'type': 'Class',
  'desc': '''The key feature of the monk is her ability to fight unarmed and unarmored. Thanks to her rigorous training, she can strike as hard as if she were armed and strike faster than a warrior with a sword. Though a monk casts no spells, she has a magic of her own. She channels a subtle energy, called ki, which allows her to perform amazing feats. The monk's best-known feat is her ability to stun an opponent with an unarmed blow. A monk also has a preternatural awareness that allows her to dodge an attack even if she is not consciously aware of it. As a monk gains experience and power, her mundane and ki-oriented abilities grow, giving her more and more power over herself and, sometimes, over others.''',
  'Alignment': ('LawfulGood', 'LawfulNeural', 'LawfulEvil'),
  'Hit Die': 'd8',
  'Base Attack Bonus': 'Medium.',
  'High Saves': 'All.',
  'Weapon Proficiencies': ('Club', 'LightCrossbow',  'HeavyCrossbow', 'Dagger', 'Handaxe', 'Javelin', 'Kama', 'Quarterstaff', 'Shuriken', 'Sling'),
  'Armor Proficiencies': (),
  'Skill Points': 4,
  'Class Skills': ('Concentration', 'CraftAlchemy', 'CraftTrap', 'Diplomacy', 'Hide', 'Listen', 'Lore', 'MoveSilently', 'Parry', 'Spot', 'Tumble'),
  'bonus': (
    (1, ('Feat', ('Monk AC Bonus', 'Flurry of Blows', 'Improved Unarm Strike'))),
    (2, ('Feat', 'Evasion')),
    (3, ('Feat', ('Fast Movement','Still Mind'))),
    (4, ('Feat', 'Ki Strike')),
    (5, ('Feat', 'Purity of Body')),
    (7, ('Feat', 'Wholeness of Body')),
    (9, ('Feat', 'Improved Evasion')),
    (11, ('Feat', 'Diamond Body')),
    (13, ('Feat', 'Diamond Soul')),
    (15, ('Feat', 'Quivering Palm')),
    (19, ('Feat', 'Empty Body')),
    (20, ('Feat', 'Perfect Self')),
  ),
}
