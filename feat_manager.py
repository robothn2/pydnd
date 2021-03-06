#coding: utf-8
import warnings

class FeatGroup:
  def __init__(self, unit, name):
    self.name = name
    self.owner = unit
    self.members = {}
    self.params = []
    self.forWeapon = False

  def __addSingleParam(self, param):
    if param not in self.params:
      self.params.append(param)

  def addMember(self, feat, param):
    if len(self.members) == 0:
      self.forWeapon = hasattr(feat, 'forWeapon')
    self.members[feat.name] = feat
    if feat.nameMember and feat.nameMember not in self.params:
      self.params.append(feat.nameMember)

    if isinstance(param, (str, int)):
      self.__addSingleParam(param)
    elif isinstance(param, (tuple, list)):
      for p in param:
        self.__addSingleParam(p)

    #print(repr(self.owner), 'add feat:', feat.name, ', new param:', param, ', final params:', self.params)

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

  def deriveFeats(self, unit):
    derived = {}
    for featName,feat in self.members.items():
      if callable(feat.deriveFeat):
        derives = feat.deriveFeat(feat, unit, None, params=self.params)
        if isinstance(derives, dict):
          derived.update(derives)
    if derived:
      print('derive feats:', derived, ' from group:', self.name)
    return derived

  def apply(self, unit, kwargs):
    #print(repr(unit), 'apply feat group:', self.name, ', members:', str(self.members.keys()))
    for featName, feat in self.members.items():
      if not feat.apply:
        continue

      if 'weapon' in kwargs:
        if self.forWeapon:
          print('  feat weapon:', featName)
          feat.apply(self, unit, feat, params=self.params, **kwargs)
      else:
        if not self.forWeapon:
          print('  feat normal:', featName)
          feat.apply(self, unit, None, params=self.params, **kwargs)


class FeatManager:
  def __init__(self, unit):
    self.owner = unit
    self.featGroups = {}

  def __repr__(self):
    ret = ''
    for groupName, featGroup in self.featGroups.items():
      ret += groupName + repr(featGroup.params) + ','
    return ret

  def addFeat(self, featNameFull, featParams = None):
    feat = self.owner.ctx['Feat'].get(featNameFull)
    if not feat:
      #warnings.warn('unknown feat: ' + featNameFull)
      return None

    featGroup = self.featGroups.get(feat.group)
    if not featGroup:
      #print('create feat group:', feat.group, 'for ', feat.name)
      featGroup = FeatGroup(self.owner, feat.group)
      self.featGroups[feat.group] = featGroup

    #print(repr(self.owner), 'add feat', feat.name, 'to group', feat.group)
    if isinstance(featParams, dict):
      featGroup.addMember(feat, featParams.get(featNameFull))
    else:
      featGroup.addMember(feat, featParams)
    return feat

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

  def deriveFeats(self, unit):
    deriveFeats = {}
    for _,group in self.featGroups.items():
      derives = group.deriveFeats(unit)
      if isinstance(derives, dict):
        deriveFeats.update(derives)

    for featName, featParam in deriveFeats.items():
      self.addFeat(featName, featParam)

  def apply(self, **kwargs):
    self.deriveFeats(self.owner)
    for groupName, featGroup in self.featGroups.items():
      featGroup.apply(self.owner, kwargs)
