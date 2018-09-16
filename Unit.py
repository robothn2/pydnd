#coding: utf-8
import warnings
from common import Props
from CombatManager import CombatManager

class Unit:
    def __init__(self, ctx):
        self.ctx = ctx
        self.props = Props.Props({'dead': False, 'weapon': 'unarmed',
                                  'ac': 0, 'ab': 0, 'hp': 0,
                                  'feats': {}, 'buffs': {}})
        self.modifier = Props.Modifier({'ArmorClass': {'Natural': {'BaseArmor': 10}}, 'HitPoint': {}})
        self.combat = CombatManager(self)

    def update(self, deltaTime):
        self.combat.update(deltaTime)

    def setProp(self, key, value):
        self.props[key] = value

    def getProp(self, key):
        if key in self.props:
            return self.props[key]
        return None

    def grantSpellClass(self, spellClass, className):
        if 'spells' not in self.props:
            self.props['spells'] = {}

        spellsEntry = self.props['spells']
        if spellClass not in spellsEntry:
            spellsEntry[spellClass] = {}

        spellsClassEntry = spellsEntry[spellClass]
        if className not in spellsClassEntry:
            spellsClassEntry[className] = {}

    def grantSpells(self, spellClass, className, spells):
        pass

    def addFeat(self, featName, featParam = []):
        if featName not in self.ctx['protosFeat']:
            warnings.warn('unknown feat: %s' % featName)
            return False

        if type(featParam) == list and len(featParam) > 0:
            for _, featHintName in enumerate(featParam):
                if len(featName) < len(featHintName) and featName == featHintName[0:len(featName)]:
                    param = featHintName[len(featName)+1:-1]
                    self.modifier.mergeBranchList(('Feats', featName), param)
                    return True

        self.modifier.mergeBranchList(('Feats', featName), featParam)
        return True

    def addFeats(self, feats, featsHint = []):
        for _, featName in enumerate(feats):
            hitHint = False
            for _, featHintName in enumerate(featsHint):
                if len(featName) < len(featHintName) and featName == featHintName[0:len(featName)]:
                    featParam = featHintName[len(featName)+1:-1]
                    self.addFeat(featName, featParam)
                    break

            if not hitHint:
                self.addFeat(featName)

    def hasFeats(self, feats):
        featsExist = self.modifier['Feats'].keys()
        for _, featName in enumerate(feats):
            if featName not in featsExist:
                return False
        return True

    def getClassLevel(self, className = None):
        if type(className) == str:
            if className in self.props['classes']:
                return self.props['classes'][className]['level']
            return 0
        return self.props.sumFieldValue('classes', 'level')

    def getAttackBonus(self, target):
        return self.getProp('ab') # for Creature
    def getArmorClass(self, target):
        return self.getProp('ac') # for Creature

    def hasBuff(self, buffName):
        return False

    def addEnemy(self, enemy):
        self.combat.addEnemy(enemy)

    def applyDamages(self, damages):
        damageTotal = damages.calcTotal()
        print(self.getProp('name'), 'accept damage', damageTotal, ' info', damages)
        self._applyDamage(damageTotal)

    def _applyDamage(self, damageTotal):
        hpOld = int(self.getProp('hp'))
        hpNew = hpOld - damageTotal
        if hpNew < 0:
            hpNew = 0
        print(self.getProp('name'), 'hp changed:', hpOld, '->', hpNew)
        self.setProp('hp', hpNew)
        if hpNew == 0:
            self.setProp('dead', True)
            print(self.getProp('name'), 'dead')

if __name__ == '__main__':
    unit = Unit()
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
