#coding: utf-8
from Models import register_spell

def __cast(spell, caster, target, **kwargs):
    target.buffs.addBuff(caster, spell, kwargs)

def __buffApply(spell, caster, target, **kwargs):
    level = caster.calc.calcPropValue('Caster.Level', caster)
    value = max(1, min(3, int(level / 3)))
    target.calc.addSource('AttackBonus.Additional', name=spell.nameBuff, calcInt=value)
    target.calc.addSource('Damage.Additional', name=spell.nameBuff, calcInt=lambda caster,target: ('Magical', spell.nameBuff, value))

def __buffUnapply(spell, caster, target, **kwargs):
    target.calc.removeSource('AttackBonus.Additional', spell.nameBuff)
    target.calc.removeSource('Damage.Additional', spell.nameBuff)

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
                   buffDuration=lambda caster, **kwargs: 60.0,
                   buffApply=__buffApply,
                   buffUnapply=__buffUnapply,
                   )
