#coding: utf-8
import warnings

class FeatGroup:
    def __init__(self, name):
        self.name = name
        self.members = {}
        self.params = []
    def addMember(self, unit, feat, param):
        self.members[feat.name] = feat
        self.params.append(feat.name)
        if hasattr(feat, 'nameMember'):
            self.params.append(feat.nameMember)
        if param is str:
            self.params.append(param)
        if hasattr(feat, 'apply'):
            print(repr(unit), 'apply feat', feat.name, 'to', ', params', self.params)
            feat.apply(feat.name, unit, feat, self.params)

    def removeMember(self, unit, feat):
        featName = feat.name if hasattr(feat, 'name') else feat
        if not featName:
            return
        featExist = self.members.get(featName)
        if not featExist:
            return

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

    def addFeat(self, featNameFull, featParams = None):
        feat = self.owner.ctx['Feat'].get(featNameFull)
        if not feat:
            warnings.warn('unknown feat: ' + featNameFull)
            return False

        featGroup = self.featGroups.get(feat.group)
        if featGroup is None:
            featGroup = FeatGroup(feat.group)
            self.featGroups[feat.group] = featGroup

        print(repr(self.owner), 'add feat', feat.nameFull, 'to group', feat.group)
        params = None
        if featParams is str or featParams is int:
            params = featParams
        elif featParams is dict:
            params = featParams.get(featNameFull)

        featGroup.addMember(self.owner, feat, params)
        return True

    def removeFeat(self, featNameFull):
        pass

    def getAvailableFeats(self):
        pass

    def applyToWeapon(self, weapon, hand):
        for groupName, featGroup in self.featGroups.items():
            featGroup.applyToWeapon(self.owner, weapon, hand)
