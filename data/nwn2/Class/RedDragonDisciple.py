#coding: utf-8

protos = [{
  'name': 'Red Dragon Disciple',
  'type': 'Class',
  'desc': '''It is known that certain dragons can take humanoid form and even have humanoid lovers. Sometimes a child is born of this union, and every child of that child unto the thousandth generation claims a bit of dragon blood, be it ever so small. Usually, little comes of it, though mighty sorcerers occasionally credit their powers to draconic heritage. For some, however, dragon blood beckons irresistibly. These characters become dragon disciples, who use their magical power as a catalyst to ignite their dragon blood, realizing its fullest potential. Members of this prestige class draw on the potent blood of red dragons coursing in their veins. Though red dragons are among the most cruel and evil creatures on Faerûn, red dragon disciples may be of any alignment.''',
  'Hit Die': 'd12',
  'Base Attack Bonus': 'Medium.',
  'High Saves': 'Fortitude and Will.',
  'Skill Points': 2,
  'Class Skills': ('Concentration', 'CraftAlchemy', 'CraftArmor', 'CraftTrap', 'CraftWeapon', 'Diplomacy', 'Listen', 'Lore', 'Parry', 'Search', 'Spellcraft', 'Spot'),
  'prerequisite': (
    ('Skill', 'Lore', 8),
    ('ClassAny', ('Bard', 'Sorcerer'))
  ),
  'bonus': (
    (1, ('Feat', ('Natural Armor Increase', 'Draconic Ability Scores'))),
    (3, ('Feat', 'Breath Weapon')),
    (5, ('Feat', 'Blind-Fight')),
    (10, ('Feat', 'Half-Dragon')),
  ),
}]

def __applyDraconicAbilityScores(feat, caster, target, **kwargs):
  level = caster.getClassLevel('RedDragonDisciple')

  strAdd = 0
  if level == 10:
    strAdd = 8
  elif level >= 4:
    strAdd = 4
  elif level >= 2:
    strAdd = 2
  if strAdd > 0:
    caster.calc.updatePropIntSource('Ability.Str.Base', feat.name, strAdd)

  if level >= 7:
    caster.calc.updatePropIntSource('Ability.Con.Base', feat.name, 2)
  if level >= 8:
    caster.calc.updatePropIntSource('Ability.Int.Base', feat.name, 2)
def __unapplyDraconicAbilityScores(feat, caster, target, **kwargs):
  caster.calc.removeSource('Ability.Str.Base', feat.name)
  caster.calc.removeSource('Ability.Con.Base', feat.name)
  caster.calc.removeSource('Ability.Int.Base', feat.name)

def __applyNaturalArmorIncrease(feat, caster, target, **kwargs):
  level = caster.getClassLevel('RedDragonDisciple')
  value = int((level + 2) / 3)
  caster.calc.updatePropIntSource('ArmorClass.Natural', feat.name, value)
def __unapplyNaturalArmorIncrease(feat, caster, target, **kwargs):
  caster.calc.removeSource('ArmorClass.Natural', feat.name)

def __applyHalfDragon(feat, caster, target, **kwargs):
  caster.calc.addSource('Vision.Dark', name=feat.name, calcInt=60)
  caster.calc.addSource('Immunity.Sleep', name=feat.name, calcInt=1)
  caster.calc.addSource('Immunity.Paralysis', name=feat.name, calcInt=1)
  caster.calc.addSource('Reduction.Fire', name=feat.name, calcInt=-1)
def __unapplyHalfDragon(feat, caster, target, **kwargs):
  caster.calc.removeSource('Vision.Dark', name=feat.name)
  caster.calc.removeSource('Immunity.Sleep', name=feat.name)
  caster.calc.removeSource('Immunity.Paralysis', name=feat.name)
  caster.calc.removeSource('Reduction.Fire', name=feat.name)

protos.extend([
  {
    'name': 'Draconic Ability Scores',
    'type': 'Feat', 'category': 'Class',
    'apply': __applyDraconicAbilityScores,
    'unapply': __unapplyDraconicAbilityScores,
    'prerequisite': [('Ability', 'Dex', 13)],
    'specifics': '''As the red dragon disciple's oneness with his draconic blood increases, his ability scores improve significantly. At 2nd level, he gains a +2 to Strength. At 4th level, this bonus increases to +4. At 7th level, the red dragon disciple gains a +2 to Constitution, and at 8th level he gains +2 Intelligence. Finally, at 10th level, he gains an additional +4 bonus to Strength (for a total of +8).''',
  },
  {
    'name': 'Natural Armor Increase',
    'type': 'Feat', 'category': 'Class',
    'apply': __applyNaturalArmorIncrease,
    'unapply': __unapplyNaturalArmorIncrease,
    'specifics': '''At 1st level, the red dragon disciple's skin toughens and begins to grow scaly, granting him a +1 natural armor bonus to AC. This bonus improves to +2 at 4th level, +3 at 7th level, and +4 at 10th level.''',
  },
  {
    'name': 'Half-Dragon',
    'type': 'Feat', 'category': 'Class',
    'apply': __applyHalfDragon,
    'unapply': __unapplyHalfDragon,
    'specifics': '''At 10th level, the red dragon disciple's transformation is complete. He becomes a half-dragon, and gains darkvision as well as immunity to sleep, paralysis, and fire.''',
  },
])
