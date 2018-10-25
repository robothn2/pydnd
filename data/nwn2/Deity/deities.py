#coding: utf-8
from Models import Deity

def _addDeity(protos, deity):
    protos['Deity'][deity.name] = deity

def register(protos):
    _addDeity(protos, Deity(
        'Leira',
         aliases = 'The Guardian of Liars, Lady of the Mists, The Lady of Deception, The Mistshadow, The Mist Maiden, Mother of Illusionists',
         alignment = tuple('ChaoticNeutral'),
         portfolio = ('Deception', 'Illusion', 'Mist', 'Shadow'),
         favoredWeapon = 'Kukri',
        ))
