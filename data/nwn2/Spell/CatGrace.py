#coding: utf-8
from Models import register_spell

def __cast(source, caster, target, spell, metaMagics):
    target.buffs.addBuff(caster, spell, metaMagics)

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
                   buffDuration=lambda caster, buff: 60.0 * caster.getClassLevel(),
                   buffApply=lambda source, caster, target, metaMagics: target.calc.addSource('Ability.Dex.Buff', name=source, calcInt=6 if 'Empower' in metaMagics else 4),
                   buffUnapply=lambda source, target: target.calc.removeSource('Ability.Dex.Buff', source),
                   )
