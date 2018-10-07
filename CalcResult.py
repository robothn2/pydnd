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

    def calcTotal(self):
        damageTotal = self.modifier.sumSource('Type')
        multiplier = Props.sumIntValue(self.modifier.sumSource('Multiplier'))
        if multiplier > 0.01:
            damageTotal = int(damageTotal * multiplier)
        return damageTotal

class Result:
    def __init__(self, name):
        self.modifier = Props.Modifier()
        self.name = name

    def addSingleSource(self, source, value):
        self.modifier[source] = value

    def addBaseSources(self, modifier):
        sources = modifier.getSource([self.name, 'Base'])
        for sourceName, value in sources.items():
            self.modifier[sourceName] = value

    def addAdditionalSources(self, modifier):
        for sourceName, value in modifier.getSource([self.name, 'Additional']).items():
            self.modifier[sourceName] = value

    def addConditionalTargetSources(self, modifier, caster, target):
        sources = modifier.getSource(['Conditional', 'Target', self.name])
        for sourceName, cond in sources.items():
            cond[0](caster, target, cond[1], self)

    def calcTotal(self):
        return Props.sumIntValue(self.modifier)

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
