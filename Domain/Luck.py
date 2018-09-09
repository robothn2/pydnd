#coding: utf-8

proto = {
    'name': 'Luck',
    'desc': '''Clerics who take the Luck domain are gifted with incredible fortune.''',
    'SpecialAbility': '''Luck of heroes: The cleric gains +1 to all saves and +1 to AC.''',
    'BonusSpells': '''The cleric gains access to the following spells at the specified spell level: freedom of movement (3), greater spell mantle (8).'''
}

def apply(unit):
    print('apply cleric domain %s' % proto['name'])
    unit.addFeat('LuckOfHeroes')
    unit.grantSpells('Divine', 'Cleric', ['FreedomOfMovement', 'GreaterSpellMantle'])
