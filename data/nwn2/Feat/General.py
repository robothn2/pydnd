#coding: utf-8
from Models import register_feat

def register(protos):
    register_feat(protos, 'General', 'Dodge',
        apply = lambda source, unit, feat, params, kwargs: unit.calc.addSource('ArmorClass.Dodge', name=source, calcInt=1),
        unapply = lambda source, unit, feat, params, kwargs: unit.calc.removeSource('ArmorClass.Dodge', source),
        prerequisite = [('Ability', 'Dex', 13)],
        specifics = '''The character gains a +1 dodge bonus to AC against attacks from his current target or last attacker.''',
    )
    register_feat(protos, 'ArmorProficiency', 'Armor Proficiency',
        specifics = '''A character cannot equip armors they are not proficient in.''',
    )
    register_feat(protos, 'WeaponProficiency', 'Weapon Proficiency',
        specifics = '''A character cannot equip weapons they are not proficient in.''',
    )

    register_feat(protos, 'Toughness', 'Toughness',
        apply = lambda source, unit, feat, params, kwargs: unit.calc.addSource('HitPoint', name=source, calcInt=lambda caster,target: unit.getClassLevel()),
        unapply = lambda source, unit, feat, params, kwargs: unit.calc.removeSource('HitPoint', source),
        specifics = '''A character with this feat is tougher than normal, gaining one bonus hit point per level. Hit points are gained retroactively when choosing this feat.''',
    )
    register_feat(protos, 'Toughness', 'Epic Toughness',
        nameMember = 'Epic',
        apply = lambda source, unit, feat, params, kwargs: unit.calc.addSource('HitPoint', name=source, calcInt=lambda caster,target: 30),
        unapply = lambda source, unit, feat, params, kwargs: unit.calc.removeSource('HitPoint', source),
        specifics = '''The character gains +30 hit points. This feat may be taken multiple times, up to a maximum of 300 hit points.''',
    )
