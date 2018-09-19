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

def conditionDamage(caster, target, params, damages):
    race = target.getProp('race')
    #print('taget race', race, ', params', params)
    if race not in params:
        return
    damages.addSingleSource('Divine', source, Dice.rollDice(1, 6, 2))

def conditionAttackBonus(caster, target, params, result):
    if len(params) == 0:
        return
    race = target.getProp('race')
    if race not in params:
        return
    result.addSingleSource(source, 2)

def apply(unit, featParams):
    featParams = unit.getFeatParams('FavoredEnemy') # use feat params from FavoredEnemy
    print('apply feat', proto['name'], ', params', featParams)

    unit.modifier.updateSource(('Conditional', 'Target', 'Damage', source), (conditionDamage, featParams))

    unit.modifier.updateSource(('Conditional', 'Target', 'AttackBonus', source), (conditionAttackBonus, featParams))
