#coding: utf-8
from Models import register_spell

def __cast(spell, caster, target, **kwargs):
    target.buffs.addBuff(caster, spell, kwargs)

proto = {
    'InnateLevel': 2,
    'School': 'Transmutation',
    'Component': ['Verbal', 'Somatic'],
    'Save': [],
    'SpellResistance': False
}

def register(protos):
    register_spell(protos, 'Cat\'s Grace',
                   specifics='''The target creature's Dexterity is increased by +4.''',
                   prerequisite=[
                       ('ClassLevel', 'Druid', 2),
                       ('ClassLevel', 'Ranger', 2),
                       ('ClassLevel', 'Bard', 2),
                       ('ClassLevel', 'Wizard', 2),
                       ('ClassLevel', 'Sorcerer', 2),
                       ('Domain', 'Plant', 2)
                   ],
                   target='Touch',
                   range='Single',
                   cast=__cast,
                   buffDuration=lambda caster, **kwargs: 60.0 * caster.getClassLevel(),
                   buffApply=lambda spell, caster, target, **kwargs: target.calc.addSource('Ability.Dex.Buff', name=spell.nameBuff, calcInt=4),
                   buffUnapply=lambda spell, caster, target, **kwargs: target.calc.removeSource('Ability.Dex.Buff', spell.nameBuff),
                   )
