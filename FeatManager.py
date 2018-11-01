#coding: utf-8
import warnings

class FeatGroup:
    def __init__(self, unit, name):
        self.name = name
        self.owner = unit
        self.members = {}
        self.params = []

    def addMember(self, feat, param):
        self.members[feat.name] = feat
        if feat.nameMember and feat.nameMember not in self.params:
            self.params.append(feat.nameMember)
        if param is str:
            self.params.append(param)
        elif param is tuple or param is list:
            for _,p in enumerate(param):
                if p not in self.params:
                    self.params.append(p)
        print(repr(self.owner), 'apply feat:', feat.name, ', new param:', param, ', final params:', self.params)
        if hasattr(feat, 'apply'):
            feat.apply(feat.name, self.owner, feat, self.params)

    def removeMember(self, feat):
        featName = feat.name if hasattr(feat, 'name') else feat
        if not featName:
            return
        featExist = self.members.get(featName)
        if not featExist:
            return
        if hasattr(featExist, 'unapply'):
            featExist.unapply(self.owner)
        self.members.pop(featName)
        #todo: remove params from self.params

    def hasMember(self, featFullName):
        return featFullName in self.members

    def apply(self, unit):
        for featName,feat in self.members.items():
            if not hasattr(feat, 'applyToWeapon'):
                return
            print(repr(unit), 'apply feat', featName, ' params', self.params)
            feat.apply(feat.name, unit, feat, self.params)

    def applyToWeapon(self, unit, weapon, hand):
        for featName,feat in self.members.items():
            if not hasattr(feat, 'applyToWeapon'):
                return
            print(repr(unit), 'apply feat', featName, 'to weapon, params', self.params)
            feat.applyToWeapon(feat.name, unit, feat, self.params, weapon=weapon, hand=hand)

class FeatManager:
    def __init__(self, unit):
        self.owner = unit
        self.featGroups = {}

    def __repr__(self):
        ret = ''
        for groupName, featGroup in self.featGroups.items():
            ret += groupName + repr(featGroup.members) + ','
        return ret
    def addFeat(self, featNameFull, featParams = None):
        feat = self.owner.ctx['Feat'].get(featNameFull)
        if not feat:
            warnings.warn('unknown feat: ' + featNameFull)
            return False

        featGroup = self.featGroups.get(feat.group)
        if featGroup is None:
            featGroup = FeatGroup(self.owner, feat.group)
            self.featGroups[feat.group] = featGroup

        #print(repr(self.owner), 'add feat', feat.nameFull, 'to group', feat.group)
        if featParams is str or featParams is int:
            featGroup.addMember(feat, featParams)
        elif featParams is tuple or featParams is list:
            featGroup.addMember(feat, featParams)
        elif featParams is dict:
            featGroup.addMember(feat, featParams.get(featNameFull))
        return True

    def removeFeat(self, featNameFull):
        pass

    def hasFeat(self, featNameFull):
        for _, featGroup in self.featGroups.items():
            if featGroup.hasMember(featNameFull):
                return True
        return False

    def getFeatParams(self, featFullName):
        for _, featGroup in self.featGroups.items():
            if featGroup.hasMember(featFullName):
                return featGroup.params
        return []

    def getAvailableFeats(self):
        pass

    def apply(self):
        for groupName, featGroup in self.featGroups.items():
            featGroup.apply(self.owner)

    def applyToWeapon(self, weapon, hand):
        for groupName, featGroup in self.featGroups.items():
            featGroup.applyToWeapon(self.owner, weapon, hand)
