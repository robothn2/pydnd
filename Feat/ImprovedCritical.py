#coding: utf-8

proto = {
    'name': 'ImprovedCritical',
    'Type': 'General',
    'Prerequisite': 'Proficiency and Weapon Focus with selected weapon, base attack bonus +4',
    'Specifics': '''When using the weapon you selected, you gain a +4 bonus on the roll to confirm a threat.''',
    'Use': '''Automatic'''
}
source = 'Feat:' + proto['name']

def applyToWeapon(unit, featParams, weapon, hand):
    if type(featParams) != list or weapon.getItemBaseName() not in featParams:
        return

    print(source, 'affects weapon:', weapon.getItemBaseName(), ', params:', featParams)
    criticalParams = weapon.proto['BaseCriticalThreat']['params']
    rangeDiff = criticalParams[1] - criticalParams[0]
    unit.calc.addSource('Weapon.%s.CriticalRange' % hand, name=source, calcInt=rangeDiff)
