#coding: utf-8

def __apply(unit):
  source = 'Race'

  # todo: affect XP requirement on level up
  unit.calc.addSource('Level.Adjustment', name=source, calcInt=2)

  unit.calc.addSource('Ability.Dex.Base', name=source, calcInt=2)
  unit.calc.addSource('Ability.Int.Base', name=source, calcInt=2)
  unit.calc.addSource('Ability.Cha.Base', name=source, calcInt=2)
  unit.calc.addSource('Ability.Con.Base', name=source, calcInt=-2)

  unit.calc.addSource('Skill.Listen', name=source, calcInt=2)
  unit.calc.addSource('Skill.Search', name=source, calcInt=2)
  unit.calc.addSource('Skill.Spot', name=source, calcInt=2)

  unit.calc.addSource('SavingThrow.Will', name=source, calcInt=2)

  unit.calc.addSource('SpellResistance', upstream='Class.Level', name=source, calcPost=lambda value: 11 + value)

  unit.addFeat('Darkvision')
  unit.addFeat('Weapon Proficiency', ['Longsword', 'Rapier', 'Longbow', 'Shortbow'])
  unit.addFeat('Favored Class', 'Wizard')

protos = {
  'name': 'Drow',
  'type': 'Race',
  'desc': '''Descended from the original dark-skinned elven subrace called the Illythiiri, the drow were cursed into their present appearance by the good elven deities for following the goddess Lolth down the path to evil and corruption. Also called dark elves, the drow have black skin that resembles polished obsidian and stark white or pale yellow hair. They commonly have very pale eyes in shades of lilac, silver, pink, and blue. They also tend to be smaller and slimmer than most elves.''',
  'LevelAdjustment': 2,
  'FavoredClass': 'Wizard',
  'apply' : __apply,
}
