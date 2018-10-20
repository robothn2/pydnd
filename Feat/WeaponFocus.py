#coding: utf-8

proto = {
    'name': 'WeaponFocus',
    'Type': 'General',
    'Prerequisite': 'Proficiency with the chosen weapon type, base attack bonus +1 or higher.',
    'RequiredFor': 'Weapon Specialization (fighter only).',
    'Specifics': '''A character with this feat is particularly skilled with a specific weapon, gaining a +1 attack bonus with it.''',
    'Use': '''Automatic. This feat may be selected multiple times, but the effects do not stack. It applies to a new weapon in each case.''',
    'Special': '''Halflings and gnomes are small creatures and as such they can never use the following large weapons: greataxes, greatswords, halberds, scythes, spears, and warmaces.'''
}
source = 'Feat:' + proto['name']

def matchRequirements(unit):
    if unit.calc.calcPropValue('AttackBonus.Base') < 1:
        return False
    return not unit.getFeatParams('WeaponProficiency')

def availableParams(unit):
    if not unit.hasFeat('WeaponProficiency'):
        return []

    weapons = unit.getFeatParams('WeaponProficiency')
    race = unit.getProp('race')
    if race not in ['Gnomes', 'Halflings']:
        return weapons

    # Halflings and gnomes cant use large weapons
    weaponsAvailable = []
    for _, weaponBaseName in weapons:
        weaponProto = unit.ctx['protosWeapon'][weaponBaseName]
        if weaponProto.proto['WeaponSize'] != 'Large':
            weaponsAvailable.append(weaponBaseName)
    return weaponsAvailable

def applyToWeapon(unit, featParams, weapon, hand):
    if type(featParams) != list or weapon.getItemBaseName() not in featParams:
        return

    print(source, 'affects weapon:', weapon.getItemBaseName(), ', params:', featParams)
    unit.calc.addSource('AttackBonus.' + hand, name='WeaponFocus', calcInt=1)
    if 'Greater' in featParams:
        unit.calc.addSource('AttackBonus.' + hand, name='GreaterWeaponFocus', calcInt=1)
    if 'Epic' in featParams:
        unit.calc.addSource('AttackBonus.' + hand, name='EpicWeaponFocus', calcInt=2)
