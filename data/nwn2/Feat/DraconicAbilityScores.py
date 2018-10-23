#coding: utf-8

proto = {
    'name': 'DraconicAbilityScores',
    'Type': 'Class',
    'Specifics': '''As the red dragon disciple's oneness with his draconic blood increases, his ability scores improve significantly. At 2nd level, he gains a +2 to Strength. At 4th level, this bonus increases to +4. At 7th level, the red dragon disciple gains a +2 to Constitution, and at 8th level he gains +2 Intelligence. Finally, at 10th level, he gains an additional +4 bonus to Strength (for a total of +8).''',
    'Use': '''Automatic'''
}
source = 'Feat:' + proto['name']

def apply(unit, featParams):
    level = unit.getClassLevel('RedDragonDisciple')

    strAdd = 0
    if level == 10:
        strAdd = 8
    elif level >= 4:
        strAdd = 4
    elif level >= 2:
        strAdd = 2
    if strAdd > 0:
        unit.calc.updatePropIntSource('Ability.Str.Base', source, strAdd)

    if level >= 7:
        unit.calc.updatePropIntSource('Ability.Con.Base', source, 2)
    if level >= 8:
        unit.calc.updatePropIntSource('Ability.Int.Base', source, 2)
