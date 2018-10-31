#coding: utf-8
from Models import Race

name = 'Yuan-ti Pureblood'

def __apply(unit):
    source = 'Race:' + name

    unit.calc.addSource('Level.Adjustment', name=source, calcInt=2)

    unit.calc.addSource('Ability.Dex.Base', name=source, calcInt=2)
    unit.calc.addSource('Ability.Int.Base', name=source, calcInt=2)
    unit.calc.addSource('Ability.Cha.Base', name=source, calcInt=2)

    unit.calc.addSource('ArmorClass.Natural', name=source, calcInt=1)

    unit.calc.addSource('SpellResistance', upstream='Class.Level', name=source, calcPost=lambda value: 11 + value)

    unit.addFeat('Darkvision')
    unit.addFeat('Alertness')
    unit.addFeat('Blind-Fight')
    unit.addFeat('Favored Class', 'Ranger')

proto = {
    'desc': '''The yuan-ti are descended from humans whose bloodlines have been mingled with those of snakes. Their evilness, cunning, and ruthlessness are legendary. Yuan-ti constantly scheme to advance their own dark agendas. They are calculating and suave enough to form alliances with other evil creatures when necessary, but they always put their own interests first.\nYuan-ti that can pass for humans with suitable clothing, cosmetics, and magic are known as Purebloods. These creatures are usually charged with infiltrating humanoid societies and managing covert operations that require direct contact with humanoids.''',
    'LevelAdjustment': 2,
    'FavoredClass': 'Ranger',
    'apply' : __apply,
}

def register(protos):
    protos['Race'][name] = Race(name, **proto)
