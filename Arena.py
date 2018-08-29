#coding: utf-8
import Character
import Creature
import Feats

ctx = {}
ctx['protosFeats'] = Feats.FeatPrototypes()
ctx['protosCreatures'] = Creature.CreaturePrototypes()

if __name__ == '__main__':
    player = Character.Character(ctx)
    player.BuildLevel1('human', 'female', 20, 'Lora', 'Craft', 'Ranger', 'Chaotic Neutral', 'Leira',
                     {'str': 16, 'dex': 14, 'con':10, 'int': 16, 'wis': 8, 'cha':  18},
                     {'Heal': 4, 'Intimidate': 4, 'Hide':4, 'MoveSilent': 4, 'Spot': 4, 'Listen': 4, 'Tumble': 4, 'Spellcraft': 4, 'UseMagicDevice': 4},
                     ['FavordEnemy:Humans', 'Dodge'])

    monster = Creature.Creature(ctx['protosCreatures'].zombie)
