#coding: utf-8
import Apply

proto = {
    'name': 'TwoWeaponFighting',
    'Type': 'General',
    'Prerequisite': 'Dex 17, Two-Weapon Fighting, base attack bonus +6 or higher.',
    'Specifics': '''The character with this feat is able to get extra off-hand attacks.''',
    'Use': 'Automatic'
}
source = 'Feat:' + proto['name']

def applyToWeapon(unit, featParams, weapon, hand):
    print('apply feat %s' % proto['name'])
    if hand == 'TwoHand':
        return
    if hand == 'OffHand':
        weaponMH = unit.calc.getObject(('Weapon', 'MainHand'))
        if weaponMH:
            unit.calc.addSource('AttackBonus.MainHand', name='Feat:TwoWeaponFighting', calcInt=-4)
            unit.calc.addSource('AttackBonus.OffHand', name='Feat:TwoWeaponFighting', calcInt=-4)
            if weapon.proto['WeaponSize'] in ['Tiny', 'Small']:
                unit.calc.addSource('AttackBonus.MainHand', name='Feat:TwoWeaponFighting', calcInt=2)
                unit.calc.addSource('AttackBonus.OffHand', name='Feat:TwoWeaponFighting', calcInt=2)

            if 'Perfect' in featParams:
                Apply.apply_weapon_attacks(weapon, unit, hand)
            elif 'Improved' in featParams:
                Apply.apply_weapon_attacks(weapon, unit, hand, 2)
            else:
                Apply.apply_weapon_attacks(weapon, unit, hand, 1)