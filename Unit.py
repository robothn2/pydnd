#coding: utf-8
import warnings
from common import Props
from CombatManager import CombatManager
from BuffManager import BuffManager
from PropCalculator import PropCalculator
from FeatManager import FeatManager

class Unit:
    def __init__(self, ctx):
        self.ctx = ctx
        self.calc = PropCalculator(ctx)
        self.props = Props.Props({'dead': False, 'hp': 0, 'xp': 0})
        self.modifier = Props.Modifier({'ArmorClass': {'Base': {'Natural': {'BaseArmor': 10}}}, 'HitPoint': {}})
        self.modifierBuff = Props.Modifier()
        self.combat = CombatManager(self)
        self.buffs = BuffManager(self)
        self.feats = FeatManager(self)

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

    def addAccessSpellClass(self, className):
        pass

    def addAccessSpell(self, className, spells = []):
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

    def matchRaces(self, races):
        race = self.getProp('race')
        return race in races

    def getClassLevel(self, className = None):
        classLevels = self.calc.getProp('Class.Level')
        if type(className) == str:
            return classLevels.calcSingleSource(className, self, None)
        return classLevels.calcValue(self, None)

    def printProp(self, key):
        print(key, ':', self.calc.calcPropValue(key, self, None))

    def getAttackBonus(self, target, hand):
        return self.calc.calcPropValue('AttackBonus.Additional', self, target) \
             + self.calc.calcPropValue('AttackBonus.' + hand, self, target)

    def getArmorClass(self, target):
        return self.calc.calcPropValue('ArmorClass', self, target)

    def addBuff(self, caster, buffProto):
        self.buffs.addBuff(caster, buffProto)
        return True

    def hasBuff(self, buffName):
        return False

    def activate(self, name):
        feat = self.calc.getPropSource('Spell.Activable', name)
        if feat:
            print('Activate ability:', name)
            feat.calcInt.activate(self)
            return

        feat = self.calc.getPropSource('Spell.Charges', name)
        if feat:
            print('Cast spell-like feat:', name)
            feat.calcInt.activate(self)
            return

        print('No activable ability found:', name)

    def deactivate(self, name):
        activableAbility = self.calc.getPropSource('Spell.Activable', name)
        if not activableAbility:
            print('No activable ability found:', name)
            return

        print('Deactivate ability:', name)
        activableAbility.calcInt.deactivate(self)

    def addEnemy(self, enemy):
        self.combat.addEnemy(enemy)

    def applyDamages(self, damages):
        damageTotal = damages.calcTotal()
        print(self.getName(), ', damage', damageTotal, ' info', damages)
        # todo: damage reduction
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
