#coding: utf-8
import json
import csv
import warnings

class CsvLoader:
    def __init__(self, csvPath, dump = False):
        self.d = {}
        try:
            records = csv.reader(open(csvPath, encoding='utf-8'))
            headers = next(records)
            for line in records:
                obj = { h: line[i] for i, h in enumerate(headers) if line[i] }
                if 'name' in obj:
                    self.d[obj['name']] = obj
        except Exception as e:
            warnings.warn('csv load error: {}, for path: {}'.format(str(e), csvPath))

        if dump:
            print(json.dumps(self.d, indent=4))

    def __contains__(self, name):
        return name in self.d
    def __getattr__(self, name):
        return self.d[name]

if __name__ == '__main__':
    creatures = CsvLoader(r'../data/beastiary.csv', True)
    feats = CsvLoader(r'../data/feats.csv', True)
