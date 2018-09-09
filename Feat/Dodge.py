#coding: utf-8

proto = {
    'name': 'Dodge',
    'Type': 'General',
    'Prerequisite': 'Dex 13+',
    'RequiredFor': 'Mobility and Spring Attack',
    'Specifics': '''The character gains a +1 dodge bonus to AC against attacks from his current target or last attacker.''',
    'Use': '''Automatic, though a condition that negates a Dexterity bonus to AC also negates any dodge bonuses. Multiple dodge bonuses (different feats, racial bonuses) are cumulative.'''
}

def matchRequirements(unit):
    return unit.modifier.sumSource(('Abilities', 'Dex'), ['Base']) >= 13

def apply(unit, featParams):
    print('apply feat %s' % proto['name'])
    unit.modifier.updateSource(('ArmorClass', 'Dodge', 'Feat:' + proto['name']), 1)

def applyAgainstTarget(caster, target):
    # todo: current target or last attacker
    return True
