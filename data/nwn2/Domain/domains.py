#coding: utf-8
from Models import Domain

def _addDomain(protos, domain):
    protos['Domain'][domain.name] = domain

def register(protos):
    _addDomain(protos, Domain(
        'Air',
         desc = '''Clerics of the Air domain move with the subtlety of the breeze and gain the ability to cast electrical damage spells.''',
         bonus = (
            ('Feat', 'Uncanny Dodge', '', '''The cleric receives the weapon focus feat for their deity's favored weapon. They are also proficient with that weapon even if clerics normally are not. If their deity's favored weapon is unarmed strike, they gain the improved unarmed strike feat.'''),
            ('SpellAccess', 'Cleric', ('Call Lightning', 'Chain Lightning')),
        )))
    _addDomain(protos, Domain(
        'Good',
         desc = 'Clerics who take the Good domain inspire their allies to heroism and are granted spells that protect against and bind evil creatures.',
         bonus = (
            ('Feat', 'Aura of Courage', '', 'The cleric is immune to fear and all allies receive a +4 saving throw bonus against fear.'),
            ('SpellAccess', 'Cleric', ('Magic Circle Against Evil', 'Lesser Planar Binding')),
        )))
    _addDomain(protos, Domain(
        'Healing',
        desc='Clerics who take the Healing domain are able to cure wounds more effectively than their brethren, and they gain access to cure spells at a faster rate.',
        bonus=(
            ('Feat', 'Empower Healing', '', 'The following healing spells are cast as if with the Empower Spell feat: CureMinorWounds, CureLightWounds, CureModerateWounds, CureSeriousWounds, and CureCriticalWounds.'),
            ('SpellAccess', 'Cleric', ('Cure Serious Wounds', 'Heal')),
        )))
    _addDomain(protos, Domain(
        'Luck',
         desc = 'Clerics who take the Luck domain are gifted with incredible fortune.',
         bonus = (
            ('Feat', 'Luck of Heroes'),
            ('SpellAccess', 'Cleric', ('Freedom of Movement', 'Greater Spell Mantle')),
        )))
    _addDomain(protos, Domain(
        'Protection',
         desc = 'Clerics who take the Protection domain are able to shield themselves from harm using their special abilities and spells.',
         bonus = (
            ('Feat', 'Divine Protection', '', '''Once per day, the cleric is able to cast an improved sanctuary spell-like ability that sets the save DC at 10 + Charisma modifier + cleric level. The effect has a duration of 1 round per caster level + the cleric's Charisma modifier.'''),
            ('SpellAccess', 'Cleric', ('Lesser Globe of Invulnerability', 'Energy Immunity'))
        )))
    _addDomain(protos, Domain(
        'Strength',
         desc = 'Clerics who take the Strength domain are able to boost their Strength with divine energy, and gain access to spells that make them stronger and more resilient.',
         bonus = (
            ('Feat', 'Divine Strength', '', '''Once per day, the cleric may gain a bonus to Strength equal to 2 + 1 per 3 class levels. This effect has a duration of 5 rounds + the cleric's Charisma modifier.'''),
            ('SpellAccess', 'Cleric', ('Bull\'s Strength', 'Divine Power'))
        )))
    _addDomain(protos, Domain(
        'Time',
         desc = 'Clerics who take the Time domain are quick to act.',
         bonus = (
            ('Feat', 'Improved Initiative', '', 'The cleric receives a bonus to initiative rolls'),
            ('SpellAccess', 'Cleric', ('Haste', 'Premonition'))
        )))
