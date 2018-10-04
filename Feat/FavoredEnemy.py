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
    if not target.matchRaces(params):
        return None

    bonus = int(caster.getClassLevel('Ranger') / 5)
    if bonus == 0:
        bonus = 1
    damages.addSingleSource('Divine', source, bonus)

def conditionSkill(caster, target, params):
    if not target.matchRaces(params):
        return None

    bonus = int(caster.getClassLevel('Ranger') / 5)
    return 1 if bonus == 0 else bonus

def apply(unit, featParams):
    print('apply feat', proto['name'], ', params', featParams)

    # todo: custom calculator for damage(dict)
    unit.calc.addSource('Damage.Additional', name=source, calcResult=lambda caster,target,damages: conditionDamage(caster, target, featParams, damages), noCache=True)

    unit.calc.addSource('Skill.Listen', name=source, calcInt=lambda caster,target: conditionSkill(caster, target, featParams), noCache=True)
    unit.calc.addSource('Skill.Spot', name=source, calcInt=lambda caster,target: conditionSkill(caster, target, featParams), noCache=True)
    unit.calc.addSource('Skill.Taunt', name=source, calcInt=lambda caster,target: conditionSkill(caster, target, featParams), noCache=True)
