#coding: utf-8

proto = {
    'name': 'Leira',
    'Aliases': 'The Guardian of Liars, Lady of the Mists, The Lady of Deception, The Mistshadow, The Mist Maiden, Mother of Illusionists',
    'Alignment': 'Chaotic Neutral',
    'Portfolio': 'Deception, illusion, mist, shadow',
    'FavoredWeapon': 'Kukri'
}

def matchRequirements(unit):
    alignment = unit.getProp('alignment')
    return alignment == proto['Alignment']
