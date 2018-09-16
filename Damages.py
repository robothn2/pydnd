#coding: utf-8
from common import Props

class Damages:
    def __init__(self):
        self.modifier = Props.Modifier()
    def __str__(self):
        return str(self.modifier)

    def addSingleSource(self, damageType, source, value):
        self.modifier.updateSource(('Type', damageType, source), value)
    def addMultiplier(self, source, value):
        self.modifier.updateSource(('Multiplier', source), value)
    def addMultipliers(self, sources):
        for k,v in sources.items():
            self.modifier.updateSource(('Multiplier', k), v)

    def addModifierSources(self, modifier, sourcePaths):
        addtionalSources = modifier.getSource(['Damage', 'Additional'])
        for dmgType, dmgSources in addtionalSources.items():
            self.modifier.mergeBranchDict(('Type', dmgType), dmgSources)

    def calcTotal(self):
        damageTotal = self.modifier.sumSource('Type')
        multiplier = Props.sumIntValue(self.modifier.sumSource('Multiplier'))
        if multiplier > 0.01:
            damageTotal = int(damageTotal * multiplier)
        return damageTotal

if __name__ == '__main__':
    dmgs = Damages()
    """
    """
    modifierChar = Props.Modifier()
    modifierChar.updateSource(('Damage', 'Additional', 'Physical', 'Ability:Str'), 4)
    modifierWeapon = Props.Modifier()
    modifierWeapon.updateSource(('Damage', 'Additional', 'Magical', 'WeaponEnhancement'), 2)
    modifierWeapon.updateSource(('Damage', 'Additional', 'Sonic', 'WeaponDamageBonus'), 5)

    dmgs.addSingleSource('Physical', 'WeaponBaseDamage', 6)
    dmgs.addModifierSources(modifierChar, ('Damage', 'Additional'))
    dmgs.addModifierSources(modifierWeapon, ('Damage', 'Additional'))
    dmgs.addMultiplier('WeaponBaseMultiplier', 2)
    dmgs.addMultiplier('Feat:IncreaseMultiplier', 2)
    dmgs.addMultiplier('Buff:Keen', 1)
    print(dmgs.calcTotal(), dmgs.modifier)
