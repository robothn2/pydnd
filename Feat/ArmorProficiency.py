#coding: utf-8

proto = {
    'name': 'ArmorProficiency',
    'Type': 'General',
    'Prerequisite': 'None',
    'Specifics': '''A character cannot equip armors they are not proficient in.'''
}
source = 'Feat:' + proto['name']

def matchRequirements(unit):
    return True

def apply(unit, featParams):
    print('apply feat %s' % proto['name'])