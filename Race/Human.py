#coding: utf-8

proto = {
    'name': 'Human',
    'desc': '''Humans are the most adaptable of the common races. Short generations and a penchant for migration and conquest mean they are very physically diverse as well. Skin shades range from nearly black to very pale, hair from black to blond, and facial hair (for men) from sparse to thick. Humans are often unorthodox in their dress, sporting unusual hairstyles, fanciful clothes, tattoos, and the like.''',
    'RacialTraits': '''- Quick to Master: One extra feat at 1st level.\n- Skilled: 4 extra skill points at 1st level, plus 1 additional skill point at each following level.\n- Favored Class: Any. When determining whether a multiclass human suffers an XP penalty, his highest-level class does not count.'''
}

def apply(unit):
    print('apply race %s' % proto['name'])
    unit.addFeat('QuickToMaster')
    unit.addFeat('Skilled')
    unit.addFeat('FavoredClass', 'Any')
