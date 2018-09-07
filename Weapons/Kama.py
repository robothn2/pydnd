#coding: utf-8

proto = {
    'name': 'Kama',
    'desc': '''As with many weapons, the kama was adapted for combat by the peasants that used them as farming implements, often because they were forbidden from owning swords or the like.''',
    'BaseDamage': {'desc': '1d6', 'params': [1, 6]},
    'BaseCriticalThreat': {'desc': '19-20/x2', 'params': [19, 20, 2]},
    'BaseDamageType': 'Slashing',
    'WeaponSize': 'Small',
    'FeatRequired': 'Exotic',
    'Weight': 2.0
}

def apply(unit, weapon):
    print('apply weapon %s' % proto['name'])
