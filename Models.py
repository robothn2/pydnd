#coding: utf-8
import regex,warnings,copy
from Dice import rollDice
import Apply

def _parseHighSaves(text):
    return (0.5 if text.find('Fortitude') >= 0 or text.find('All') >= 0 else 0.25,
            0.5 if text.find('Reflex') >= 0 or text.find('All') >= 0 else 0.25,
            0.5 if text.find('Will') >= 0 or text.find('All') >= 0 else 0.25)
def _parseBaseAttackBonus(text):
    if text.find('High') >= 0:
        return 1.0
    return 0.75 if text.find('Medium') >= 0 else 0.5
def _parseHitDie(text):
    return int(regex.match(r"d(\d+)", text).groups()[0])
def _parseWeaponProficiencies(text):
    return text
def _parseArmorProficiencies(text):
    return text
def _parseSkillPoints(text):
    return text
def _parseClassSkills(text):
    return text
def _parse(kwargs, key, func):
    if key not in kwargs:
        return None
    return func(kwargs.pop(key))

def name_canonical(nameFull):
    name = nameFull.replace('\'s', '').replace('-', '')
    words = name.split(' ')
    return ''.join(list(map(lambda word: word.capitalize(), words)))

def _applyTupleResource(res, unit, **kwargs):
    if res is not tuple:
        return
    if res[0] is function:
        # support (_addDeityWeaponFocus, ...),
        res[0](unit)
        return
    if res[0] is str:
        if res[0] == 'Feat':
            if res[1] is str:
                # support ('Feat', 'Breath Weapon')
                featName = res[1]
                unit.addFeat(featName, kwargs.get(featName))
            elif res[1] is tuple:
                # support ('Feat', ('Natural Armor Increase', 'Draconic Ability Scores'))
                for _,featName in enumerate(res[1]):
                    unit.feats.addFeat(featName)
        elif res[0] == 'SpellAccess':
            # support ('SpellAccess', 'Cleric', ('Magic Circle Against Evil', 'Lesser Planar Binding'))
            unit.addAccessSpell(res[1], res[2])
        elif res[0] == 'SpellType':
            # support ('SpellType', 'Divine', ...)
            unit.addAccessSpellClass(res[1])
        elif res[0] == 'Domain':
            # support ('Domain', 2)
            for _, domainName in enumerate(kwargs['domains']):
                if domainName not in unit.ctx['Domain']:
                    continue
                domainProto = unit.ctx['Domain'][domainName]
                domainProto.apply(unit)

def isRequirementsMatch(requirements, unit):
    if not requirements:
        return True

    for _,cond in enumerate(requirements):
        if cond is not tuple or len(cond) < 2:
            continue

        # check Ability
        if cond[0] == 'Ability':
            # support ('Ability', 'Dex', 13),
            if unit.calc.calcPropValue('Ability.' + cond[1] + '.Base', unit, None) < cond[2]:
                return False

        # check Skill
        elif cond[0] == 'Skill':
            # support ('Skill', 'Tumble', 5),
            if unit.calc.calcPropValue('Skill.' + cond[1], 'Builder') < cond[2]:
                return False

        # check Level
        elif cond[0] == 'Level':
            # support ('Level', 21)
            if unit.getClassLevel() < cond[1]:
                return False

        # check ClassLevel
        elif cond[0] == 'ClassLevel':
            if cond[1] is str and cond[2] is int:
                # support ('ClassLevel', 'Ranger, 21)
                if unit.getClassLevel(cond[1]) < cond[2]:
                    return False
            else:
                return False

        # check ClassAny
        elif cond[0] == 'ClassAny':
            clsMatched = False
            if cond[1] is tuple:
                # support ('ClassAny', ('Bard', 'Sorcerer'))
                for _1,cls in enumerate(cond[1]):
                    if unit.getClassLevel('Sorcerer') > 0:
                        clsMatched = True
                        break
            if not clsMatched:
                return False

        # check BaseAttackBonus
        elif cond[0] == 'BaseAttackBonus':
            # support ('BaseAttackBonus', 5)
            if unit.calc.calcPropValue('AttackBonus.Base', unit) < cond[2]:
                return False

        # check Feat
        elif cond[0] == 'Feat':
            if cond[1] is tuple:
                # support ('Feat', ('Dodge', 'Mobility', 'CombatExpertise', 'SpringAttack', 'WhirlwindAttack')),
                if not unit.hasFeats(cond[1]):
                    return False
            elif cond[1] is str:
                if not unit.hasFeat(cond[1]):
                    return False
            else:
                return False

        # custom condition
        elif cond[0] == 'Function':
            if cond[1] is not function or not cond[1](unit):
                # support ('Function', function, 'Weapon Focus in a melee weapon')
                return False
        else:
            warnings.warn('unknown condition ' + repr(cond))
            return False
    return True

class ModelBase:
    def __init__(self, name, **kwargs):
        self.nameFull = name
        self.name = name_canonical(name)
        self.model = type(self.name, (), kwargs)

class Race(ModelBase):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)

class Deity(ModelBase):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)

class Class(ModelBase):
    def __init__(self, name, **kwargs):
        self.bab = _parse(kwargs, 'Base Attack Bonus', _parseBaseAttackBonus)
        self.hd = _parse(kwargs, 'Hit Die', _parseHitDie)
        (self.fortitude, self.reflex, self.will) = _parse(kwargs, 'High Saves', _parseHighSaves)
        self.weapons = _parse(kwargs, 'Weapon Proficiencies', _parseWeaponProficiencies)
        self.armors = _parse(kwargs, 'Armor Proficiencies', _parseArmorProficiencies)
        self.skillPoints = _parse(kwargs, 'Skill Points', _parseSkillPoints)
        self.classSkills = _parse(kwargs, 'Class Skills', _parseClassSkills)
        super().__init__(name, **kwargs)
        self.spellType = None
        for _,bonus in enumerate(kwargs['bonus']):
            # (1, ('SpellType', 'Arcane', ...))
            if bonus[1][0] == 'SpellType':
                self.spellType = (bonus[1][1], bonus[0])

        # print(self)

    def isAvailable(self, unit):
        if not hasattr(self.model, 'Requirements'):
            return True
        return isRequirementsMatch(self.model.requirements, unit)

    def levelUp(self, unit, level, **choices):
        print('apply', self.name, 'level', level)
        if level == 1:
            print(self.weapons, self.armors)
            unit.addFeat('Weapon Proficiency', self.weapons)
            unit.addFeat('Armor Proficiency', self.armors)

        if not hasattr(self.model, 'bonus'):
            return
        for _,entry in enumerate(self.model.bonus):
            if entry is not tuple:
                continue
            if entry[0] == level:
                _applyTupleResource(entry[1], unit)
            elif entry[0] is function:
                if entry[0](level):
                    _applyTupleResource(entry[1], unit, **choices)

class Domain(ModelBase):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)

    def apply(self, unit):
        print('apply cleric domain %s' % self.name)
        if hasattr(self, 'bonus'):
            for _,entry in enumerate(self.bonus):
                if entry is not tuple:
                    continue
                _applyTupleResource(entry, unit)

class Feat(ModelBase):
    def __init__(self, name, **kwargs):
        self.category = kwargs.pop('Type') if 'Type' in kwargs else 'General'
        super().__init__(name, **kwargs)
        self.group = self.name # default group name is self

    def isAvailable(self, unit):
        if not hasattr(self.model, 'prerequisite'):
            return True
        return isRequirementsMatch(self.model.prerequisite, unit)

    def apply(self, source, unit, feat, params):
        if hasattr(self.model, 'apply'):
            self.model.apply(feat.name, unit, feat, params)
    def unapply(self, target = None):
        pass
    def active(self, caster):
        pass
    def deactive(self, caster):
        pass

def register_feat(protos, groupName, featName, **kwargs):
    feat = Feat(featName, **kwargs)
    feat.group = groupName
    feat.nameMember = kwargs.pop('nameMember') if 'nameMember' in kwargs else None
    protos['Feat'][feat.nameFull] = feat

class Spell(ModelBase):
    def __init__(self, name, **kwargs):
        self.nameBuff = kwargs.pop('nameBuff') if 'nameBuff' in kwargs else name
        super().__init__(name, **kwargs)
    def apply(self, source, unit, featParams):
        pass
    def unapply(self, target = None):
        pass
    def duration(self):
        pass

def register_spell(protos, spellName, **kwargs):
    spell = Spell(spellName, **kwargs)
    protos['Spell'][spellName] = spell
    if hasattr(spell.model, 'buffDuration'):
        protos['Buff'][spell.nameBuff] = spell

class Weapon(ModelBase):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.nameBase = self.name

    def __repr__(self):
        return self.name

    def getItemBaseName(self):
        return self.nameBase

    def apply(self, unit, hand):
        Apply.apply_weapon_attacks(self, unit, hand)

        unit.calc.updateObject(('Weapon', hand), self)

        # weapon base damage
        weaponParams = self.model.damageRoll
        unit.calc.addSource('Damage.' + hand, name=self.name, calcInt=lambda caster, target: ('Physical', self.name, rollDice(1, weaponParams[1], weaponParams[0])), noCache=True)

        # weapon enhancement
        if hasattr(self.model, 'enhancement'):
            unit.calc.addSource('Weapon.%s.Additional' % hand, name='WeaponEnhancement', calcInt=('Magical', 'WeaponEnhancement', self.model.enhancement))
            unit.calc.addSource('AttackBonus.' + hand, name='WeaponEnhancement', calcInt=self.model.enhancement)

        # weapon critical parameter
        criticalParams = self.model.criticalThreat
        unit.calc.addSource('Weapon.%s.CriticalRange' % hand, name='WeaponBase', calcInt=criticalParams[0])
        unit.calc.addSource('Weapon.%s.CriticalMultiplier' % hand, name='WeaponBase', calcInt=criticalParams[1])

        # weapon related feats
        unit.feats.applyToWeapon(self, hand)

    def unapply(self, unit, hand):
        unit.calc.removeSource('Attacks', hand)

        unit.calc.removeSource('Damage.' + hand, self.name)

        unit.calc.removeSource('Weapon.%s.Additional' % hand, 'WeaponEnhancement')
        unit.calc.removeSource('Damage.' + hand, 'WeaponEnhancement')

        unit.calc.removeSource('Weapon.%s.CriticalRange' % hand, 'WeaponBase')
        unit.calc.removeSource('Weapon.%s.CriticalMultiplier' % hand, 'WeaponBase')


def register_weapon(protos, weaponName, **kwargs):
    weapon = Weapon(weaponName, **kwargs)
    protos['Weapon'][weaponName] = weapon


def create_weapon(protos, weaponName, **kwargs):
    if weaponName in protos['Weapon']:
        weapon = copy.deepcopy(protos['Weapon'][weaponName])
        if 'name' in kwargs:
            weapon.name = kwargs['name']
        elif 'enhancement' in kwargs:
            weapon.name += '+' + str(kwargs['enhancement'])
        return weapon

    # for a natural weapon, we need following keys in |props|:
    #   BaseCriticalThreat, default is [20, 20, 2], also named as 20/x2
    #   BaseDamage, default is [1,4,1], also named as 1d4
    #   BaseDamageType, default is ['Bludgeoning']
    damageRoll = kwargs.pop('damageRoll') if 'damageRoll' in kwargs else (1, 4)
    criticalThreat = kwargs.pop('criticalThreat') if 'criticalThreat' in kwargs else (0, 2)
    weaponSize = kwargs.pop('size') if 'size' in kwargs else 'Small'
    damageType = kwargs.pop('damageType') if 'damageType' in kwargs else 'Bludgeoning'
    specifics = kwargs.pop('specifics') if 'specifics' in kwargs else 'natural weapon ' + weaponName
    weapon = Weapon(weaponName, damageRoll = damageRoll, criticalThreat = criticalThreat, damageType = damageType,\
                    size = weaponSize, specifics = specifics)
    return weapon
