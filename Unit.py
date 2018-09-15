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

    def addFeat(self, featName, featParam = None):
        if featName not in self.ctx['protosFeat']:
            warnings.warn('unknown feat: %s' % featName)
            return False

        if type(featParam) == str:
            self.modifier.updateListParam(('Feats', featName), [featParam])
            return True
        if type(featParam) == list:
            self.modifier.updateListParam(('Feats', featName), featParam)
            return True
        self.modifier.updateListParam(('Feats', featName), [])
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

    def hasBuff(self, buffName):
        return False

    def addEnemy(self, enemy):
        self.combat.addEnemy(enemy)

    def applyDamages(self, damages):
        damageTotal = damages.sumSource('Type')
        multiplier = damages.sumSource('Multiplier')
        if multiplier > 0.01:
            damageTotal = int(damageTotal * multiplier)
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
