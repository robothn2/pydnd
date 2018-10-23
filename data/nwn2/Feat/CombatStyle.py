#coding: utf-8

proto = {
    'name': 'CombatStyle',
    'Type': 'Class',
    'Prerequisite': 'None',
    'Specifics': '''A Ranger can chosen TwoWeaponFighting or Archery combat style. If you chosen TwoWeaponFighting, you gain the following bonus feats: TwoWeaponFighting at 2nd level, Improved TwoWeaponFighting at 6th level, Greater TwoWeaponFighting at 11st level, and Perfect TwoWeaponFighting at 21st level. If you chosen Archery, you gain the following bonus feats: Rapid Shot at 2nd level, Manyshot at 6th level, and Improved Rapid Shot at 11th level. You gain the benefit of these feats even if you do not meet their prerequisites.''',
    'Use': '''Automatic'''
}

def matchRequirements(unit):
    return False

def apply(unit, featParams):
    pass
