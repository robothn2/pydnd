#coding: utf-8
from Models import Class, register_feat

name = 'Red Dragon Disciple'
proto = {
    'desc': '''It is known that certain dragons can take humanoid form and even have humanoid lovers. Sometimes a child is born of this union, and every child of that child unto the thousandth generation claims a bit of dragon blood, be it ever so small. Usually, little comes of it, though mighty sorcerers occasionally credit their powers to draconic heritage. For some, however, dragon blood beckons irresistibly. These characters become dragon disciples, who use their magical power as a catalyst to ignite their dragon blood, realizing its fullest potential. Members of this prestige class draw on the potent blood of red dragons coursing in their veins. Though red dragons are among the most cruel and evil creatures on Faerûn, red dragon disciples may be of any alignment.''',
    'Hit Die': 'd12',
    'Base Attack Bonus': 'Medium.',
    'High Saves': 'Fortitude and Will.',
    'Skill Points': 2,
    'Class Skills': ('Concentration', 'CraftAlchemy', 'CraftArmor', 'CraftTrap', 'CraftWeapon', 'Diplomacy', 'Listen', 'Lore', 'Parry', 'Search', 'Spellcraft', 'Spot'),
    'requirements': (
        ('Skill', 'Lore', 8),
        ('ClassAny', ('Bard', 'Sorcerer'))
    ),
    'bonus': (
        (1, ('Feat', ('Natural Armor Increase', 'Draconic Ability Scores'))),
        (3, ('Feat', 'Breath Weapon')),
        (5, ('Feat', 'Blind-Fight')),
        (10, ('Feat', 'Half-Dragon')),
    ),
}

def __applyDraconicAbilityScores(source, unit, feat, params):
    level = unit.getClassLevel('RedDragonDisciple')

    strAdd = 0
    if level == 10:
        strAdd = 8
    elif level >= 4:
        strAdd = 4
    elif level >= 2:
        strAdd = 2
    if strAdd > 0:
        unit.calc.updatePropIntSource('Ability.Str.Base', source, strAdd)

    if level >= 7:
        unit.calc.updatePropIntSource('Ability.Con.Base', source, 2)
    if level >= 8:
        unit.calc.updatePropIntSource('Ability.Int.Base', source, 2)
def __unapplyDraconicAbilityScores(source, unit, feat, params):
    unit.calc.removeSource('Ability.Str.Base', source)
    unit.calc.removeSource('Ability.Con.Base', source)
    unit.calc.removeSource('Ability.Int.Base', source)

def __applyNaturalArmorIncrease(source, unit, feat, params):
    level = unit.getClassLevel('RedDragonDisciple')
    value = int((level + 2) / 3)
    unit.calc.updatePropIntSource('ArmorClass.Natural', source, value)
def __unapplyNaturalArmorIncrease(source, unit, feat, params):
    unit.calc.removeSource('ArmorClass.Natural', source)

def __applyHalfDragon(source, unit, feat, params):
    unit.calc.addSource('Vision.Dark', name=source, calcInt=60)
    unit.calc.addSource('Immunity.Sleep', name=source, calcInt=1)
    unit.calc.addSource('Immunity.Paralysis', name=source, calcInt=1)
    unit.calc.addSource('Reduction.Fire', name=source, calcInt=-1)
def __unapplyHalfDragon(source, unit, feat, params):
    unit.calc.removeSource('Vision.Dark', name=source)
    unit.calc.removeSource('Immunity.Sleep', name=source)
    unit.calc.removeSource('Immunity.Paralysis', name=source)
    unit.calc.removeSource('Reduction.Fire', name=source)

def register(protos):
    protos['Class'][name] = Class(name, **proto)

    register_feat(protos, 'DraconicAbilityScores', 'Draconic Ability Scores',
                  type = 'Class',
                  applyGroup = __applyDraconicAbilityScores,
                  unapply = __unapplyDraconicAbilityScores,
                  specifics = '''As the red dragon disciple's oneness with his draconic blood increases, his ability scores improve significantly. At 2nd level, he gains a +2 to Strength. At 4th level, this bonus increases to +4. At 7th level, the red dragon disciple gains a +2 to Constitution, and at 8th level he gains +2 Intelligence. Finally, at 10th level, he gains an additional +4 bonus to Strength (for a total of +8).''',
                  )
    register_feat(protos, 'NaturalArmorIncrease', 'Natural Armor Increase',
                  type = 'Class',
                  applyGroup = __applyNaturalArmorIncrease,
                  unapply = __unapplyDraconicAbilityScores,
                  specifics = '''At 1st level, the red dragon disciple's skin toughens and begins to grow scaly, granting him a +1 natural armor bonus to AC. This bonus improves to +2 at 4th level, +3 at 7th level, and +4 at 10th level.''',
                  )
    register_feat(protos, 'HalfDragon', 'Half-Dragon',
                  type = 'Class',
                  applyGroup = __applyHalfDragon,
                  unapply = __unapplyHalfDragon,
                  specifics = '''At 10th level, the red dragon disciple's transformation is complete. He becomes a half-dragon, and gains darkvision as well as immunity to sleep, paralysis, and fire.''',
                  )
