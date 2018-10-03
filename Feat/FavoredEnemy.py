#coding: utf-8

proto = {
    'name': 'FavoredEnemy',
    'Type': 'Class',
    'Prerequisite': 'Ranger level 1.',
    'Specifics': '''The character gains a +1 bonus to damage rolls against their favored enemy. They also receive a +1 bonus on Listen, Spot, and Taunt checks against the favored enemy. Every 5 levels, the ranger may choose an additional Favored Enemy and all bonuses against all favored enemies increase by +1.''',
    'Use': '''Automatic'''
}
source = 'Feat:' + proto['name']

def matchRequirements(unit):
    return True

def conditionDamage(caster, target, params, damages):
    race = target.getProp('race')
    #print('taget race', race, ', params', params)
    if race not in params:
        return

    bonus = int(caster.getClassLevel('Ranger') / 5)
    if bonus == 0:
        bonus = 1
    damages.addSingleSource('Divine', source, bonus)

def conditionSkill(caster, target, params):
    race = target.getProp('race')
    print('taget race', race, ', params', params)
    if race not in params:
        return None

    bonus = int(caster.getClassLevel('Ranger') / 5)
    return 1 if bonus == 0 else bonus

def apply(unit, featParams):
    print('apply feat', proto['name'], ', params', featParams)

    # todo: custom calculator for damage(dict)
    unit.calc.addSource('Damage.Target', name=source, calcInt=conditionDamage, calcParam=featParams, noCache=True)

    # todo: support calcParam=featParams in PropSourceInt
    unit.calc.addSource('Skill.Listen', name=source, calcInt=conditionSkill, calcParam=featParams)
    unit.calc.addSource('Skill.Spot', name=source, calcInt=conditionSkill, calcParam=featParams)
    unit.calc.addSource('Skill.Taunt', name=source, calcInt=conditionSkill, calcParam=featParams)
