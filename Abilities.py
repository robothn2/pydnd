#coding: utf-8

class Abilities:
    def __init__(self, abilities, dexterity = None, constitution = None, intelligence = None, wisdom = None, charisma = None):
        self.str = 8 #strength
        self.dex = 8 #dexterity
        self.con = 8 #constitution
        self.int = 8 #intelligence
        self.wis = 8 #wisdom
        self.cha = 8 #charisma

        if type(abilities) is int:
            self.str = abilities
            self.dex = dexterity or 8
            self.con = constitution or 8
            self.int = intelligence or 8
            self.wis = wisdom or 8
            self.cha = charisma or 8

        elif type(abilities) is dict:
            for k,v in abilities.items():
                if k == 'str' or k == 'strength':
                    self.str = int(v)
                elif k == 'dex' or k == 'dexterity':
                    self.dex = int(v)
                elif k == 'con' or k == 'constitution':
                    self.con = int(v)
                elif k == 'int' or k == 'intelligence':
                    self.int = int(v)
                elif k == 'wis' or k == 'wisdom':
                    self.wis = int(v)
                elif k == 'cha' or k == 'charisma':
                    self.cha = int(v)

        elif type(abilities) is list and len(abilities) == 6:
            self.str = int(abilities[0])
            self.dex = abilities[1]
            self.con = abilities[2]
            self.int = abilities[3]
            self.wis = abilities[4]
            self.cha = abilities[5]
            
        print('  abilities:', str(self))

    def __str__(self):
        return '{} {} {} {} {} {}'.format(self.str, self.dex, self.con, self.int, self.wis, self.cha)
        
if __name__ == '__main__':
    ab = Abilities({'str': 16, 'dex': 14, 'con':10, 'int': 16, 'wis': 8, 'cha':  18})
    ab2 = Abilities({'strength': 16, 'dexterity': 14, 'constitution':10, 'intelligence': 16, 'wisdom': 8, 'charisma':  18})
    ab3 = Abilities([16, 14, 10, 16, 8, 18])
    ab4 = Abilities(16, 14, 10, 16, 8, 18)
