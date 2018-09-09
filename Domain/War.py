#coding: utf-8

proto = {
    'name': 'War',
    'desc': '''Clerics who take the War domain spend considerable time training for combat.''',
    'SpecialAbility': '''Weapon focus: The cleric receives the weapon focus feat for their deity's favored weapon. They are also proficient with that weapon even if clerics normally are not. If their deity's favored weapon is unarmed strike, they gain the improved unarmed strike feat.''',
    'BonusSpells': '''The cleric gains access to the following spells at the specified spell level: flame strike (4), power word stun (8).'''
}

def apply(unit):
    print('apply cleric domain %s' % proto['name'])
    deityName = unit.getProp('deity')
    if deityName in unit.ctx['protosDeity']:
        deityProto = unit.ctx['protosDeity'][deityName]
        weapon = deityProto.proto['FavoredWeapon']
        if weapon == 'UnarmedStrike':
            unit.addFeat('ImprovedUnarmedStrike')
        else:
            unit.addFeat(['WeaponFocus(%s)' % weapon])

    unit.grantSpells('Divine', 'Cleric', ['FlameStrike', 'PowerWordStun'])
