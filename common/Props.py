#coding: utf-8
import warnings

def makeBranch(dictExist, paths, branchDefaultValue={}):
    d = dictExist
    if type(paths) == str:
        if paths not in d:
            d[paths] = branchDefaultValue
        return d[paths]

    if type(paths) != list and type(paths) != tuple:
        raise RuntimeError('wrong parameter type for updateSource(paths)')
    cnt = len(paths)
    if cnt == 0:
        raise RuntimeError('paths is empty for updateSource')

    for i in range(cnt):
        key = paths[i]
        if i == cnt - 1:
            if key not in d:
                d[key] = branchDefaultValue
            return d[key]

        if key not in d:
            d[key] = {}
        d = d[key]

def getBranch(dictExist, paths, defaultValue = {}):
    d = dictExist
    if type(paths) == str:
        if len(paths) == 0:
            return d
        return d[paths] if paths in d else defaultValue
    if (type(paths) != list and type(paths) != tuple):
        return defaultValue

    cnt = len(paths)
    if cnt == 0:
        return defaultValue

    for i in range(cnt):
        key = paths[i]
        if i == cnt -1:
            return d[key] if key in d else defaultValue

        if key not in d:
            return defaultValue
        d = d[key]

def sumIntValue(value):
    sumValue = 0
    if type(value) == int:
        sumValue += value
    elif type(value) == dict:
        for subValue in value.values():
            sumValue += int(subValue)
    return sumValue

def mergeList(listExist, paramsToMerge):
    if type(paramsToMerge) == str:
        listExist.append(paramsToMerge)
        return
    if type(paramsToMerge) != list and type(paramsToMerge) != tuple:
        return
    cnt = len(paramsToMerge)
    if cnt == 0:
        return

    for i in range(cnt):
        value = paramsToMerge[i]
        if value not in listExist:
            listExist.append(value)

class Modifier(dict):
    # Source is a key-value pair under dict based Branch
    # Source is unique by key, updateSource has replace semantics
    def updateSource(self, paths, value):
        if type(paths) == str:
            self[paths] = value
            return
        if len(paths) == 1:
            self[paths[0]] = value
            return

        branch = makeBranch(self, paths[:-1], {})
        branch[paths[-1]] = value

    def mergeBranchDict(self, paths, branchNew):
        if type(branchNew) != dict:
            warnings.warn('wrong parameter type for mergeBranch(branchNew)')
            return

        branch = makeBranch(self, paths, {})
        branch.update(branchNew)

    def mergeBranchList(self, paths, params):
        mergeList(makeBranch(self, paths, []), params)

    def getSource(self, paths, defaultValue={}):
        return getBranch(self, paths, defaultValue)

    def sumSource(self, pathsList, includeBranchNames = None, excludeBranchNames = None):
        branch = getBranch(self, pathsList, {})
        sumValue = 0
        if type(includeBranchNames) == list:
            for _, name in enumerate(includeBranchNames):
                if name not in branch:
                    continue
                # sum sources under branch[name]
                for v in branch[name].values():
                    sumValue += sumIntValue(v)
        else:
            for key, branchSub in branch.items():
                if type(excludeBranchNames) == list and key not in excludeBranchNames:
                    continue
                # sum sources under branch
                if type(branchSub) == int:
                    sumValue += branchSub
                    continue
                for v in branchSub.values():
                    sumValue += sumIntValue(v)
        return sumValue

class Props(dict):
    def incValue(self, key, value):
        if key not in self:
            self[key] = value
            return

        self[key] += value

    def hasKey(self, key, subkey):
        if key not in self:
            return False
        return subkey in self[key]

    def hasKeyList(self, key, subKeyList):
        if key not in self:
            return False

        keyEntry = self[key]
        for i, subKey in enumerate(subKeyList):
            if subKey not in keyEntry:
                return False
        return True

    def sumFieldValue(self, key, fieldName):
        if key not in self:
            return 0
        sumField = 0
        for field in self[key].values():
            if fieldName in field:
                sumField += field[fieldName]
        return sumField

if __name__ == '__main__':
    modifier = Modifier()
    """
    modifier.mergeBranchList(('F', 'FavoredEnemy'), 'Human')
    modifier.mergeBranchList(('F', 'FavoredEnemy'), 'Dragon')
    modifier.mergeBranchList(('F', 'FavoredEnemy'), ['Undead', 'Demon'])
    print(modifier.getSource(['F']))

    modifier.updateSource(('A', 'Stt', 'Base', 'B'), 5)
    modifier.updateSource(('A', 'Stt', 'Base', 'B'), 9)
    print(modifier.getSource('A'))

    modifier.updateSource('B', [(0.0, 1, 2), (1.0, 3, 5)])
    print(modifier.getSource('B'))

    modifier.updateSource(('D', 'Additional', 'CLS'), 20)
    print(modifier.getSource(('D', 'Additional')))
    print(modifier.sumSource(('D', 'Additional')))
    """

    modifier.updateSource(('Dmg', 'Add', 'Magical', 'Enhance'), 2)
    modifier.updateSource(('Dmg', 'Add', 'Sonic', 'DamageBonus'), 5)
    dmgs = {'Magical': 1}
    print(dmgs)
