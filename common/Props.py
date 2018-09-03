#coding: utf-8

class Modifier(dict):
    def addSource(self, key, value, source = ''):
        if key not in self:
            self[key] = {source: value}
            return

        self[key][source] = value

    def addTypedSource(self, key, subtype, value, source = ''):
        if key not in self:
            self[key] = {subtype: {source: value}}
            return

        entry = self[key]
        if subtype not in entry:
            entry[subtype] = {source: value}
            return

        entrySub = entry[subtype]
        entrySub[source] = value

class Props(dict):
    def incValue(self, key, value):
        if key not in self:
            self[key] = value
            return

        self[key] += value

if __name__ == '__main__':
    modifier = Modifier({})
    modifier.addTypedSource('ArmorClass', 'Tumble', 1)
    print(modifier)

    modifier = Modifier({'ArmorClass': {}})
    modifier.addTypedSource('ArmorClass', 'Tumble', 2, 'Skills:Tumble')
    print(modifier)

    modifier = Modifier({'ArmorClass': {'Dodge': {'Dex': 2}}})
    modifier.addTypedSource('ArmorClass', 'Tumble', 2, 'Skills:Tumble')
    print(modifier)
