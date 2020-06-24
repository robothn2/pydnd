#coding: utf-8

protos = {
  'name': '''Cat's Grace''',
  'type': 'Spell',
  'InnateLevel': 2,
  'School': 'Transmutation',
  'prerequisite': [
    ('ClassLevel', 'Druid', 2),
    ('ClassLevel', 'Ranger', 2),
    ('ClassLevel', 'Bard', 2),
    ('ClassLevel', 'Wizard', 2),
    ('ClassLevel', 'Sorcerer', 2),
    ('Domain', 'Plant', 2)
  ],
  'Component': ['Verbal', 'Somatic'],
  'Target': 'Single',
  'Range': 'Touch',
  'Duration': '1 hour / level',
  'Save': [],
  'SpellResistance': False,
  'specifics': '''The target creature's Dexterity is increased by +4.''',

  'buffDuration': lambda caster, **kwargs: 60.0 * caster.getClassLevel(),
  'buffApply': lambda spell, caster, target, **kwargs: target.calc.addSource('Ability.Dex.Buff', name=spell.nameBuff, calcInt=4),
  'buffUnapply': lambda spell, caster, target, **kwargs: target.calc.removeSource('Ability.Dex.Buff', spell.nameBuff),
}
