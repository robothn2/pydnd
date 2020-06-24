#coding: utf-8

def __apply(unit):
  unit.addFeat('Quick to Master')
  unit.addFeat('Skilled')
  unit.addFeat('Favored Class', 'Any')

protos = {
  'name': 'Drow',
  'type': 'Race',
  'desc': '''Humans are the most adaptable of the common races. Short generations and a penchant for migration and conquest mean they are very physically diverse as well. Skin shades range from nearly black to very pale, hair from black to blond, and facial hair (for men) from sparse to thick. Humans are often unorthodox in their dress, sporting unusual hairstyles, fanciful clothes, tattoos, and the like.''',
  'FavoredClass': 'Any',
  'apply': __apply,
}
