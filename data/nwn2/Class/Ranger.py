#coding: utf-8
from Models import Class, Feat, register_feat
import Dice

name = 'Ranger'

def _applyFeatFavoredEnemy(source, unit, feat, params):
    bonus = max(1, int(unit.getClassLevel('Ranger') / 5))
    calcDamage = lambda caster,target: None if not target.matchRaces(featParams) else ('Divine', source, bonus)
    unit.calc.addSource('Damage.Additional', name=source, calcInt=calcDamage, noCache=True)
    calcSkill = lambda caster,target: 0 if not target.matchRaces(featParams) else max(1, int(caster.getClassLevel('Ranger') / 5))
    unit.calc.addSource('Skill.Listen', name=source, calcInt=calcSkill, noCache=True)
    unit.calc.addSource('Skill.Spot', name=source, calcInt=calcSkill, noCache=True)
    unit.calc.addSource('Skill.Taunt', name=source, calcInt=calcSkill, noCache=True)
def _unapplyFeatFavoredEnemy(source, unit, feat, params):
    unit.calc.removeSource('Damage.Additional', source)
    unit.calc.addSource('Skill.Listen', source)
    unit.calc.addSource('Skill.Spot', source)
    unit.calc.addSource('Skill.Taunt', source)

def _applyFeatBaneOfEnemies(source, unit, feat, params):
    calcDamage = lambda caster,target: None if not target.matchRaces(params) else ('Divine', source, Dice.rollDice(1, 6, 2))
    unit.calc.addSource('Damage.Additional', name=source, calcInt=calcDamage, noCache=True)
    unit.calc.addSource('AttackBonus.Additional', name=source, calcInt=lambda caster,target: 2 if target.matchRaces(params) else 0)
def _unapplyFeatBaneOfEnemies(source, unit, featParams):
    unit.calc.removeSource('Damage.Additional', source)
    unit.calc.removeSource('AttackBonus.Additional', source)

def _applyFeatCombatStyle(source, unit, feat, params):
    level = unit.getClassLevel(name)
    if 'TwoWeaponFighting' in params:
        if level >= 2:
            unit.addFeat('Two-Weapon Fighting')
        elif level >= 21:
            unit.addFeat('Perfect Two-Weapon Fighting')
    elif 'Archery' in params:
        unit.addFeat('Rapid Shot')
def _unapplyFeatCombatStyle(source, unit, feat, params):
    unit.removeFeat('Two-Weapon Fighting')
    unit.removeFeat('Perfect Two-Weapon Fighting')
    unit.removeFeat('Rapid Shot')

def _applyFeatImprovedCombatStyle(source, unit, feat, params):
    if 'TwoWeaponFighting' in params:
        unit.addFeat('Improved Two-Weapon Fighting')
    elif 'Archery' in params:
        unit.addFeat('Manyshot')
def _unapplyFeatImprovedCombatStyle(source, unit, feat, params):
    if 'TwoWeaponFighting' in params:
        unit.removeFeat('Improved Two-Weapon Fighting')
    elif 'Archery' in params:
        unit.removeFeat('Manyshot')

def _applyFeatCombatMastery(source, unit, feat, params):
    if 'TwoWeaponFighting' in params:
        unit.addFeat('Greater Two-Weapon Fighting')
    elif 'Archery' in params:
        unit.addFeat('Improved Rapid Shot')
def _unapplyFeatCombatMastery(source, unit, feat, params):
    if 'TwoWeaponFighting' in params:
        unit.removeFeat('Greater Two-Weapon Fighting')
    elif 'Archery' in params:
        unit.removeFeat('Improved Rapid Shot')

proto = {
    'desc': '''A ranger can use a variety of weapons and is quite capable in combat. His skills allow him to survive in the wilderness, to find his prey, and to avoid detection. He also has special knowledge about certain types of creatures, which makes it easier for him to find and defeat such foes. Finally, an experienced ranger has such a tie to nature that he can actually draw upon natural power to cast divine spells, much as a druid does.''',
    'Hit Die': 'd8',
    'Base Attack Bonus': 'High.',
    'High Saves': 'Fortitude and Reflex.',
    'Weapon Proficiencies': ('Simple', 'Martial'),
    'Armor Proficiencies': ('Light', 'Shield'),
    'Skill Points': 6,
    'Class Skills': ('Concentration', 'CraftAlchemy', 'CraftArmor', 'CraftTrap', 'CraftWeapon', 'Heal', 'Hide', 'Listen', 'Lore', 'MoveSilently', 'Parry', 'Search', 'SetTrap', 'Spot', 'Survival'),
    'bonus': (
        (lambda level: level == 1 or level % 5 == 0, ('Feat', 'Favored Enemy', '''At 1st level, a ranger may select a type of creature as his favored enemy. The ranger gains a +1 bonus on Bluff, Listen, Spot, and Taunt checks, and also a +1 bonus on weapon damage rolls against their favored enemy. At 5th level, and every five levels after that, the ranger can choose an additional favored enemy and gains +1 to all favored enemy bonuses.''')),
        (1, ('Feat', 'Track', 'A ranger has the ability to find and read tracks, but he moves slowly when doing so.')),
        (2, ('Feat', 'Combat Style')),
        (3, ('Feat', 'Toughness')),
        (4, ('Feat', 'Animal Companion', 'At 4th level, a ranger gains an animal companion.')),
        (4, ('SpellType', 'Divine', '''Beginning at 4th level, a ranger gains the ability to cast a small number of divine spells, which are drawn from the ranger spell list. A ranger must choose and prepare his spells in advance. To prepare or cast a spell, a ranger must have a Wisdom score equal to at least 10 + the spell level (Wis 10 for 0-level spells, Wis 11 for 1st-level spells, and so forth).''')),
        (6, ('Feat', 'Improved Combat Style')),
        (7, ('Feat', 'Woodland Stride', '''Starting at 7th level, a ranger gains a +10% movement increase when in outdoor, natural environments.''')),
        (8, ('Feat', 'Swift Tracker', '''At 8th level, a ranger can use their tracking skill and move at normal speed.''')),
        (9, ('Feat', 'Evasion', '''At 9th level, a ranger can avoid even magical and unusual attacks with great agility. If he makes a successful Reflex saving throw against an attack that normally deals half damage on a successful save (such as a red dragon's fiery breath or a fireball), he instead takes no damage. Evasion can be used only if the ranger is wearing light armor or no armor.''')),
        (11, ('Feat', 'Combat Mastery')),
        (13, ('Feat', 'Camouflage', '''At 13th level the ranger does not suffer a movement penalty for using stealth mode when in outdoor areas.''')),
        (17, ('Feat', 'Hide in Plain Sight', '''When outdoors, a 17th level ranger has the ability to use the Hide skill even when being watched and in combat.''')),
    ),
}

def register(protos):
    protos['Class'][name] = Class(name, **proto)

    # feat group: favored enemy
    register_feat(protos, 'FavoredEnemy', 'Favored Enemy',
                  type = 'Class',
                  apply = _applyFeatFavoredEnemy,
                  unapply = _unapplyFeatFavoredEnemy,
                  prerequisite = [('ClassLevel', name, 1)],
                  specifics = '''The character gains a +1 bonus to damage rolls against their favored enemy. They also receive a +1 bonus on Listen, Spot, and Taunt checks against the favored enemy. Every 5 levels, the ranger may choose an additional Favored Enemy and all bonuses against all favored enemies increase by +1.'''
                  )
    register_feat(protos, 'FavoredEnemy', 'Bane of Enemies',
                  type = 'Class',
                  apply = _applyFeatBaneOfEnemies,
                  unapply = _unapplyFeatBaneOfEnemies,
                  prerequisite = [('ClassLevel', name, 1)],
                  specifics = '''The character gains a 2d6 bonus to damage rolls and +2 attack bonus against their favored enemy.'''
                  )

    # feat group: CombatStyle
    register_feat(protos, 'CombatStyle', 'Combat Style',
                  type = 'Class',
                  applyGroup = _applyFeatCombatStyle,
                  unapply = _unapplyFeatCombatStyle,
                  prerequisite = [('ClassLevel', name, 2)],
                  specifics = '''A Ranger can chosen TwoWeaponFighting or Archery combat style. If you chosen TwoWeaponFighting, you gain the following bonus feats: TwoWeaponFighting at 2nd level, Improved TwoWeaponFighting at 6th level, Greater TwoWeaponFighting at 11st level, and Perfect TwoWeaponFighting at 21st level. If you chosen Archery, you gain the following bonus feats: Rapid Shot at 2nd level, Manyshot at 6th level, and Improved Rapid Shot at 11th level. You gain the benefit of these feats even if you do not meet their prerequisites.''',
                  )
    register_feat(protos, 'CombatStyle', 'Improved Combat Style',
                  type = 'Class',
                  applyGroup = _applyFeatImprovedCombatStyle,
                  unapply = _unapplyFeatImprovedCombatStyle,
                  prerequisite = [('ClassLevel', name, 6)],
                  specifics = '''At 6th level, a ranger's aptitude in his chosen combat style (archery or two-weapon combat) improves. If he selected archery at 2nd level, he is treated as having the Manyshot feat, even if he does not have the normal prerequisites for that feat. If the ranger selected two-weapon combat at 2nd level, he is treated as having the Improved Two-Weapon Fighting feat, even if he does not have the normal prerequisites for that feat. As before, the benefits of the ranger's chosen style apply only when he wears light or no armor. He loses all benefits of his combat style when wearing medium or heavy armor.''',
                  )
    register_feat(protos, 'CombatStyle', 'Combat Mastery',
                  type = 'Class',
                  applyGroup = _applyFeatCombatMastery,
                  unapply = _unapplyFeatCombatMastery,
                  prerequisite = [('ClassLevel', name, 11)],
                  specifics = '''At 11th level, a ranger's aptitude in his chosen combat style (archery or two-weapon combat) improves again. If he selected archery at 2nd level, he is treated as having the Improved Rapid Shot feat, even if he does not have the normal prerequisites for that feat. If the ranger selected two-weapon combat at 2nd level, he is treated as having the Greater Two-Weapon Fighting feat, even if he does not have the normal prerequisites for that feat. As before, the benefits of the ranger's chosen style apply only when he wears light or no armor. He loses all benefits of his combat style when wearing medium or heavy armor.''',
                  )
