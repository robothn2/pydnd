#coding: utf-8
import csv
import warnings

def loadCsvFile(csvPath):
    props = {}
    try:
        records = csv.reader(open(csvPath, encoding='utf-8'))
        headers = next(records)
        for line in records:
            obj = { h: line[i] for i, h in enumerate(headers) if line[i] }
            if 'name' in obj:
                props[obj['name']] = obj
    except Exception as e:
        warnings.warn('csv load error: {}, for path: {}'.format(str(e), csvPath))
    return props