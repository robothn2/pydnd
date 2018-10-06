#coding: utf-8
import Dice

proto = {
    'name': 'BaneOfEnemies',
    'Type': 'Class',
    'Prerequisite': 'Ranger level 21.',
    'Specifics': '''The character gains a 2d6 bonus to damage rolls and +2 attack bonus against their favored enemy.''',
    'Use': '''Automatic'''
}
source = 'Feat:' + proto['name']

def matchRequirements(unit):
    return unit.getClassLevel('Ranger') >= 21

def apply(unit, featParams):
    races = unit.getFeatParams('FavoredEnemy') # use feat params from FavoredEnemy
    print('apply feat', proto['name'], ', params', races)

    unit.calc.addSource('Damage.Additional', name=source, calcVoid=\
        lambda damages,caster,target: damages.addSingleSource('Divine', source, Dice.rollDice(1, 6, 2)) if target.matchRaces(races) else None)

    unit.calc.addSource('AttackBonus.Additional', name=source, calcInt=lambda caster,target: 2 if target.matchRaces(races) else 0)
