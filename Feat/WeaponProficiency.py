#coding: utf-8

proto = {
    'name': 'WeaponProficiency',
    'Type': 'General',
    'Prerequisite': 'None',
    'Specifics': '''A character cannot equip weapons they are not proficient in.'''
}
source = 'Feat:' + proto['name']

def apply(unit, featParams):
    pass
