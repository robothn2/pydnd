#coding: utf-8
from Models import register_spell

def __cast(spell, caster, target, **kwargs):
    target.buffs.addBuff(caster, spell, kwargs)

def __buffApply(spell, caster, target, **kwargs):
    level = caster.calc.calcPropValue('Caster.Level', caster, None)
    value = 3
    if level >= 13:
        value = 5
    elif level >= 7:
        value = 4
    target.calc.addSource('ArmorClass.Natural', name=spell.nameBuff, calcInt=value)

proto = {
    'InnateLevel': 2,
    'School': 'Transmutation',
    'Component': ['Verbal', 'Somatic'],
    'Duration': '1 hour / level',
    'Save': [],
    'SpellResistance': False
}

def register(protos):
    register_spell(protos, 'Barkskin',
                   specifics='''Barkskin hardens the target creature's skin, granting a natural armor bonus to Armor Class based on the caster's level: Level 1-6: +3, Level 7-12: +4, Levels 13+: +5''',
                   prerequisite=[('ClassLevel', 'Druid', 2), ('ClassLevel', 'Ranger', 2), ('Domain', 'Plant', 2)],
                   target='Single',
                   range='Touch',
                   cast=__cast,
                   buffDuration=lambda caster, **kwargs: 3600.0 * caster.getClassLevel(),
                   buffApply=__buffApply,
                   buffUnapply=lambda spell, caster, target, **kwargs: target.calc.removeSource('ArmorClass.Natural', spell.nameBuff),
                   )
