#coding: utf-8
import warnings
from common import Props
from CombatManager import CombatManager
from BuffManager import BuffManager
from PropCalculator import PropCalculator

class Unit:
    def __init__(self, ctx):
        self.ctx = ctx
        self.calc = PropCalculator(ctx)
        self.props = Props.Props({'dead': False,
                                  'ac': 0, 'ab': 0, 'hp': 0, 'xp': 0})
        self.modifier = Props.Modifier({'ArmorClass': {'Base': {'Natural': {'BaseArmor': 10}}}, 'HitPoint': {}})
        self.modifierBuff = Props.Modifier()
        self.modifierWeapon = Props.Modifier()
        self.combat = CombatManager(self)
        self.buffs = BuffManager(self)

    def __repr__(self):
        return self.getName()

    def update(self, deltaTime):
        if self.isDead():
            return

        self.buffs.update(deltaTime)
        self.combat.update(deltaTime)

    def getName(self):
        return self.props.get('name')

    def setProp(self, key, value):
        self.props[key] = value

    def getProp(self, key):
        if key in self.props:
            return self.props[key]
        return None
    def isDead(self):
        return self.props['dead']

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

        if type(featParam) == str or type(featParam) == int:
            self.modifier.mergeBranchList(('Feats', featName), featParam)
            return True

        if type(featParam) == list:
            for _, featHintName in enumerate(featParam):
                if type(featHintName) == str: #support addFeat('FavoredEnemy', ['Dragons'])
                    self.modifier.mergeBranchList(('Feats', featName), featHintName)
                    return True
                if type(featHintName) == list and len(featHintName) == 2: #support addFeat('FavoredEnemy', [['FavoredEnemy','Dragons']])
                    if featHintName[0] == featName:
                        self.modifier.mergeBranchList(('Feats', featName), featHintName[1])
                        return True

        self.modifier.mergeBranchList(('Feats', featName), [])
        return True

    def addFeats(self, feats, featsHint = []):
        for _, featName in enumerate(feats):
            hitHint = False
            for _, featHintName in enumerate(featsHint):
                if len(featName) < len(featHintName) and featName == featHintName[0:len(featName)]:
                    hitHint = True
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
    def hasFeat(self, feat):
        return feat in self.modifier['Feats']

    def getFeatParams(self, featName):
        if featName not in self.modifier['Feats']:
            return []
        return self.modifier['Feats'][featName]

    def getClassLevel(self, className = None):
        if type(className) == str:
            if className in self.props['classes']:
                return self.props['classes'][className]['level']
            return 0
        return self.props.sumFieldValue('classes', 'level')

    def getCasterLevel(self, classSpellType = 'Divine'):
        level = 0
        if 'classes' in self.props:
            for className, classInfo in self.props.get('classes', {}).items():
                if not classSpellType or classSpellType == classInfo['proto'].proto.get('SpellType'):
                    level += classInfo['level']

        return level

    def getAttackBonus(self, target):
        return self.getProp('ab') # for Creature
    def getArmorClass(self, target):
        return self.getProp('ac') # for Creature

    def addBuff(self, caster, buffProto):
        self.buffs.addBuff(caster, buffProto)
        return True

    def hasBuff(self, buffName):
        return False

    def addEnemy(self, enemy):
        self.combat.addEnemy(enemy)

    def applyDamages(self, damages):
        damageTotal = damages.calcTotal()
        print(self.getName(), 'accept damage', damageTotal, ' info', damages)
        self._applyDamage(damageTotal)

    def _applyDamage(self, damageTotal):
        hpOld = int(self.getProp('hp'))
        hpNew = hpOld - damageTotal
        if hpNew < 0:
            hpNew = 0
        print(self.getName(), 'hp changed:', hpOld, '->', hpNew)
        self.setProp('hp', hpNew)
        if hpNew == 0:
            self.setProp('dead', True)
            print(self.getName(), 'die')
