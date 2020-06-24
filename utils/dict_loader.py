#coding: utf-8
import sys


def parse_file_to_dict(path):
  dictionary = {}
  try:
    if sys.version_info[0] == 2:
      execfile(path, dictionary)
    else:
      with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
      exec(content, {}, dictionary)
  except Exception as e:
    print('Fail to load script {}, {}'.format(path, str(e)))
    raise e

  return dictionary

