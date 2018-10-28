#coding: utf-8
from Models import register_spell

def __cast(source, caster, target, spell, metaMagics):
    target.buffs.addBuff(caster, spell, metaMagics)

def __buffApply(source, caster, target, metaMagics):
    level = caster.calc.calcPropValue('Caster.Level', caster, None)
    value = max(1, min(3, int(level / 3)))
    target.calc.addSource('AttackBonus.Additional', name=source, calcInt=value)
    target.calc.addSource('Damage.Additional', name=source, calcInt=lambda caster,target: ('Magical', source, value))

def __buffUnapply(source, target):
    target.calc.removeSource('AttackBonus.Additional', source)
    target.calc.removeSource('Damage.Additional', source)

proto = {
    'InnateLevel': 1,
    'School': 'Evocation',
    'Component': ['Verbal', 'Somatic'],
    'Duration': '1 minute',
    'Save': [],
    'SpellResistance': False
}

def register(protos):
    register_spell(protos, 'Divine Favor',
                   specifics='''You gain a +1 bonus to attack and a +1 magical damage bonus for every three caster levels you have (minimum +1, maximum of +3).''',
                   prerequisite=[('ClassLevel', 'Cleric', 1), ('ClassLevel', 'Paladin', 1)],
                   target='Caster',
                   range='Personal',
                   cast=__cast,
                   buffDuration=lambda caster, buff: 60.0,
                   buffApply=__buffApply,
                   buffUnapply=__buffUnapply,
                   )
