#coding: utf-8

'''
ab1 = abilities_parse({'Str': 16, 'Dex': 14, 'Con': 10, 'Int': 16, 'Wis': 8, 'Cha': 18})
ab2 = abilities_parse({'strength': 16, 'dexterity': 14, 'constitution': 10, 'intelligence': 16, 'wisdom': 8, 'charisma': 18})
ab3 = abilities_parse([16, 14, 10, 16, 8, 18])
ab4 = abilities_parse(16, 14, 10, 16, 8, 18)
'''
def abilities_parse(abilities, dexterity = None, constitution = None, intelligence = None, wisdom = None, charisma = None):
    d = {'Str':8, 'Dex':8, 'Con':8, 'Int':8, 'Wis':8, 'Cha':8}

    if type(abilities) is int:
        d['Str'] = abilities
        d['Dex'] = dexterity or 8
        d['Con'] = constitution or 8
        d['Int'] = intelligence or 8
        d['Wis'] = wisdom or 8
        d['Cha'] = charisma or 8

    elif type(abilities) is dict:
        for k,v in abilities.items():
            if k == 'Str' or k == 'strength':
                d['Str'] = int(v)
            elif k == 'Dex' or k == 'dexterity':
                d['Dex'] = int(v)
            elif k == 'Con' or k == 'constitution':
                d['Con'] = int(v)
            elif k == 'Int' or k == 'intelligence':
                d['Int'] = int(v)
            elif k == 'Wis' or k == 'wisdom':
                d['Wis'] = int(v)
            elif k == 'Cha' or k == 'charisma':
                d['Cha'] = int(v)

    elif type(abilities) is list and len(abilities) == 6:
        d['Str'] = int(abilities[0])
        d['Dex'] = int(abilities[1])
        d['Con'] = int(abilities[2])
        d['Int'] = int(abilities[3])
        d['Wis'] = int(abilities[4])
        d['Cha'] = int(abilities[5])

    return d

def abilities_modifier(props, key):
    return int((int(props[key]) - 10) / 2)

def abilities_apply(props, modifier):
    modifier.addTypedSource('AttackBonus', 'Str', abilities_modifier(props, 'Str'), 'Ability:Str')
    modifier.addTypedSource('ArmorClass', 'Dex', abilities_modifier(props, 'Dex'), 'Ability:Dex')
    modifier.addTypedSource('HitPoint', 'Con', abilities_modifier(props, 'Con'), 'Ability:Con')
