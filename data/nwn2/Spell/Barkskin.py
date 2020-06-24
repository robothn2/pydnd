#coding: utf-8

def __buffApply(spell, caster, target, **kwargs):
    level = caster.calc.calcPropValue('Caster.Level', caster, None)
    value = 3
    if level >= 13:
        value = 5
    elif level >= 7:
        value = 4
    target.calc.addSource('ArmorClass.Natural', name=spell.nameBuff, calcInt=value)

protos = {
  'name': 'Barkskin',
  'type': 'Spell',
  'InnateLevel': 2,
  'School': 'Transmutation',
  'prerequisite': [('ClassLevel', 'Druid', 2), ('ClassLevel', 'Ranger', 2), ('Domain', 'Plant', 2)],
  'Component': ['Verbal', 'Somatic'],
  'Target': 'Single',
  'Range': 'Touch',
  'Duration': '1 hour / level',
  'Save': [],
  'SpellResistance': False,
  'specifics': '''Barkskin hardens the target creature's skin, granting a natural armor bonus to Armor Class based on the caster's level: Level 1-6: +3, Level 7-12: +4, Levels 13+: +5''',

  'buffDuration': lambda caster, **kwargs: 3600.0 * caster.getClassLevel(),
  'buffApply': __buffApply,
  'buffUnapply': lambda spell, caster, target, **kwargs: target.calc.removeSource('ArmorClass.Natural', spell.nameBuff),
}
