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
    if unit.modifier.sumSource('AttackBonus', ['Base']) < 1:
        return False
    return unit.hasFeats(['WeaponProficiency'])

def availableParams(unit):
    if not unit.hasFeats(['WeaponProficiency']):
        return []

    weapons = unit.modifier.getSource(['Feats', 'WeaponProficiency'])
    race = unit.getProp('race')
    if race not in ['Gnomes', 'Halflings']:
        return weapons;

    # Halflings and gnomes cant use large weapons
    weaponsAvailable = []
    for _, weaponBaseName in weapons:
        weaponProto = unit.ctx['protosWeapon'][weaponBaseName]
        if weaponProto.proto['WeaponSize'] != 'Large':
            weaponsAvailable.append(weaponBaseName)
    return weaponsAvailable

def condition(caster, weapon, params):
    #print('condition of', proto['name'], ': weapon', weapon.proto['name'], ', params', params)
    if not params or weapon.proto['name'] not in params:
        return

    weapon.modifier.updateSource(('AttackBonus', 'Additional', source), 1)
    #print('modifier for weapon', weapon.props['name'], weapon.modifier)

def apply(unit, featParams):
    print('apply feat %s' % proto['name'])
    unit.modifier.updateSource(('Conditional', 'Weapon', source), (condition, featParams))
