#coding: utf-8

proto = {
    'name': 'War',
    'desc': '''Clerics who take the War domain spend considerable time training for combat.''',
    'BonusFeats': [
        ('Feat', 'WeaponFocus', '''The cleric receives the weapon focus feat for their deity's favored weapon. They are also proficient with that weapon even if clerics normally are not. If their deity's favored weapon is unarmed strike, they gain the improved unarmed strike feat.'''),
    ],
    'BonusSpells': ['FlameStrike', 'PowerWordStun'],
}

def apply(unit):
    print('apply cleric domain %s' % proto['name'])
    deityName = unit.getProp('deity')
    if deityName in unit.ctx['protosDeity']:
        deityProto = unit.ctx['protosDeity'][deityName]
        weapon = deityProto.proto['FavoredWeapon']
        print('deity:', deityName, 'weapon:', weapon)
        if weapon == 'UnarmedStrike':
            unit.addFeat('ImprovedUnarmedStrike')
        else:
            unit.addFeat('WeaponFocus', weapon)

    unit.addAccessSpell('Cleric', ['FlameStrike', 'PowerWordStun'])
