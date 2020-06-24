#coding: utf-8
from utils.csv_loader import load_csv_file
from utils.dict_loader import parse_file_to_dict
import models
import os


def _reg_proto(proto, protos):
  if 'type' not in proto:
    return False

  t = proto.pop('type')
  name = proto.pop('name')
  if t == 'Feat':
    feat = models.Feat(name, **proto)
    protos['Feat'][feat.nameBuff] = feat
  elif t == 'Spell':
    spell = models.Spell(name, **proto)
    protos['Spell'][spell.nameBuff] = spell
    #support buff with the same name as the spell that generate it
    if hasattr(proto, 'buffDuration'):
      protos['Buff'][spell.nameBuff] = spell
  elif t == 'Weapon':
    weapon = models.Weapon(name, **proto)
    protos['Weapon'][weapon.nameFull] = weapon
  elif t == 'Race':
    race = models.Race(name, **proto)
    protos['Race'][race.nameFull] = race
  elif t == 'Class':
    cls = models.Class(name, **proto)
    protos['Class'][cls.nameFull] = cls
  elif t == 'Deity':
    deity = models.Deity(name, **proto)
    protos['Deity'][deity.nameFull] = deity
  elif t == 'Domain':
    domain = models.Domain(name, **proto)
    protos['Domain'][domain.nameFull] = domain
  else:
    return False
  return True

def _load_script_folder(protos, scriptFolderPath):
  for folder, _, fileNames in os.walk(scriptFolderPath, followlinks=False):
    for fileName in fileNames:
      if not fileName.endswith('.py'):
        continue

      script = os.path.join(folder, fileName)
      mod = parse_file_to_dict(script)
      proto = mod.get('protos')
      loaded_cnt = 0
      if isinstance(proto, dict):
        if _reg_proto(proto, protos):
          loaded_cnt += 1
      elif isinstance(proto, list):
        for p in proto:
          if isinstance(p, dict) and _reg_proto(p, protos):
            loaded_cnt += 1
      if loaded_cnt == 0:
        print(' no protos loaded from {}'.format(script))
        print(mod)

ctx = {
  'secondsPerTurn': 6.0,
  'secondsPerRound': 6.0,
  'Abilities': ('Str', 'Dex', 'Con', 'Int', 'Wis', 'Cha'),

  'Deity': {},
  'Domain': {},
  'Feat': {},
  'Class': {},
  'Race': {},
  'Weapon': {},
  'Spell': {},
  'Buff': {},
  'Skill': {},
  'Creature': {},
}

_load_script_folder(ctx, 'data/nwn2/Race')
_load_script_folder(ctx, 'data/nwn2/Class')
_load_script_folder(ctx, 'data/nwn2/Domain')
_load_script_folder(ctx, 'data/nwn2/Deity')
_load_script_folder(ctx, 'data/nwn2/Feat')
_load_script_folder(ctx, 'data/nwn2/Spell')
_load_script_folder(ctx, 'data/nwn2/Weapon')
ctx['Skill'] = load_csv_file(r'data/skills.csv')
ctx['Creature'] = load_csv_file(r'data/beastiary.csv')
