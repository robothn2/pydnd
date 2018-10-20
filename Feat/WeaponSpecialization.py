#coding: utf-8

proto = {
    'name': 'WeaponSpecialization',
    'Type': 'Special',
    'Prerequisite': 'Must be a fighter, base attack bonus +4, Weapon Focus in the chosen weapon group.',
    'Specifics': '''A character with this feat is particularly skilled with a specific weapon, gaining a +1 attack bonus with it.''',
    'Use': '''Automatic. This feat may be selected multiple times, but the effects do not stack. It applies to a new weapon in each case.''',
}
source = 'Feat:' + proto['name']

def matchRequirements(unit):
    if unit.calc.calcPropValue('AttackBonus.Base') < 4:
        return False
    return unit.hasFeat('WeaponFocus')

def applyToWeapon(unit, featParams, weapon, hand):
    if type(featParams) != list or weapon.getItemBaseName() not in featParams:
        return

    print(source, 'affects weapon:', weapon.getItemBaseName(), ', params:', featParams)
    unit.calc.addSource('Damage.'+ hand, name='WeaponSpecialization', calcInt=('Physical', 'WeaponSpecialization', 2))
    if 'Greater' in featParams:
        unit.calc.addSource('Damage.'+ hand, name='GreaterWeaponSpecialization', calcInt=('Physical', 'GreaterWeaponSpecialization', 2))
    if 'Epic' in featParams:
        unit.calc.addSource('Damage.'+ hand, name='EpicWeaponSpecialization', calcInt=('Physical', 'EpicWeaponSpecialization', 2))
