#coding: utf-8
from utils.csv_loader import load_csv_file
from utils.dict_loader import parse_file_to_dict
from protos import register_proto
import os


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
        if register_proto(proto, protos):
          loaded_cnt += 1
      elif isinstance(proto, (list,tuple)):
        for p in proto:
          if isinstance(p, dict) and register_proto(p, protos):
            loaded_cnt += 1

      if loaded_cnt == 0:
        print(' no protos loaded from {}'.format(script))

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
