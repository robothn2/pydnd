#coding: utf-8
from Models import register_feat

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
        weaponProto = unit.ctx['Weapon'][weaponBaseName]
        if weaponProto.proto['WeaponSize'] != 'Large':
            weaponsAvailable.append(weaponBaseName)
    return weaponsAvailable

def __applyWeaponFocus(source, unit, feat, params, **kwargs):
    weapon = kwargs.get('weapon')
    hand = kwargs.get('hand')
    if params is not list or weapon.getItemBaseName() not in params:
        return

    print(source, 'affects weapon:', weapon.getItemBaseName(), ', params:', params)
    unit.calc.addSource('AttackBonus.' + hand, name='WeaponFocus', calcInt=1)
    if 'Greater' in params:
        unit.calc.addSource('AttackBonus.' + hand, name='GreaterWeaponFocus', calcInt=1)
    if 'Epic' in params:
        unit.calc.addSource('AttackBonus.' + hand, name='EpicWeaponFocus', calcInt=2)
    if 'ImprovedCritical' in params:
        criticalParams = weapon.proto['BaseCriticalThreat']['params']
        rangeDiff = criticalParams[1] - criticalParams[0]
        unit.calc.addSource('Weapon.%s.CriticalRange' % hand, name=source, calcInt=rangeDiff)
def __unapplyWeaponFocus(source, unit, feat, params):
    unit.calc.removeSource('AttackBonus.TwoHand', feat.nameMember)
    unit.calc.removeSource('AttackBonus.MainHand', feat.nameMember)
    unit.calc.removeSource('AttackBonus.OffHand', feat.nameMember)


def register(protos):
    register_feat(protos, 'WeaponFocus', 'Weapon Focus',
                  apply=__applyWeaponFocus,
                  unapply=__unapplyWeaponFocus,
                  prerequisite=[('BaseAttackBonus', 1), ('Feat', 'Weapon Proficiency')],
                  specifics='''A character with this feat is particularly skilled with a specific weapon, gaining a +1 attack bonus with it.''',
                  )
    register_feat(protos, 'WeaponFocus', 'Greater Weapon Focus',
                  nameMember='Greater',
                  prerequisite=[('ClassLevel', 'Fighter', 8), ('Feat', 'Weapon Focus')],
                  specifics='''This feat grants an additional +1 to hit bonus with the selected weapon. This stacks with all other bonuses to attack roll (including Weapon Focus). This feat can be taken multiple times, but each time the effect applies to a new type of weapon.''',
                  )
    register_feat(protos, 'WeaponFocus', 'Epic Weapon Focus',
                  type='Epic',
                  nameMember='Epic',
                  prerequisite=[('Level', 21), ('Feat', 'Greater Weapon Focus')],
                  specifics='''The character gains +4 bonus to all attack rolls made using the selected weapon. This feat can be taken multiple times, but it applies to a different weapon each time. This bonus replaces that of Weapon Focus and Greater Weapon Focus.''',
                  )
    register_feat(protos, 'WeaponFocus', 'Improved Critical',
                  nameMember='ImprovedCritical',
                  prerequisite=[('Feat', 'Weapon Focus'), ('BaseAttackBonus', 4)],
                  specifics='''Combat ability doubles the critical threat range with a given weapon. A longsword that normally threatens a critical on a roll of 19-20 would now threaten a critical on a roll of 17-20.''',
                  )
