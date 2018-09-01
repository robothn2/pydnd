#coding: utf-8

'''
ab1 = parse_abilities({'Str': 16, 'Dex': 14, 'Con': 10, 'Int': 16, 'Wis': 8, 'Cha': 18})
ab2 = parse_abilities({'strength': 16, 'dexterity': 14, 'constitution': 10, 'intelligence': 16, 'wisdom': 8, 'charisma': 18})
ab3 = parse_abilities([16, 14, 10, 16, 8, 18])
ab4 = parse_abilities(16, 14, 10, 16, 8, 18)
'''
def parse_abilities(abilities, dexterity = None, constitution = None, intelligence = None, wisdom = None, charisma = None):
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
        d['Dex'] = abilities[1]
        d['Con'] = abilities[2]
        d['Int'] = abilities[3]
        d['Wis'] = abilities[4]
        d['Cha'] = abilities[5]

    print(d)
    return d
