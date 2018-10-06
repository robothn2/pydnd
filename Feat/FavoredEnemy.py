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

def calcDamage(caster, target, params, damages):
    if not target.matchRaces(params):
        return

    bonus = max(1, int(caster.getClassLevel('Ranger') / 5))
    damages.addSingleSource('Divine', source, bonus)

def calcSkill(caster, target, params):
    if not target.matchRaces(params):
        return 0

    return max(1, int(caster.getClassLevel('Ranger') / 5))

def apply(unit, featParams):
    print('apply feat', proto['name'], ', params', featParams)

    unit.calc.addSource('Damage.Additional', name=source, calcVoid=lambda damages,caster,target: calcDamage(caster, target, featParams, damages), noCache=True)

    unit.calc.addSource('Skill.Listen', name=source, calcInt=lambda caster,target: calcSkill(caster, target, featParams), noCache=True)
    unit.calc.addSource('Skill.Spot', name=source, calcInt=lambda caster,target: calcSkill(caster, target, featParams), noCache=True)
    unit.calc.addSource('Skill.Taunt', name=source, calcInt=lambda caster,target: calcSkill(caster, target, featParams), noCache=True)
