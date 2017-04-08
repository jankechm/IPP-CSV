import sys

import src.err as err
import csv

class CSV(object):
    """CSV"""
    _table = dict()

    def __init__(self, ops, file=None):
        self._file_address = file
        self._ops = ops

    def open(self):
        if (self._ops['input']):
            try:
                self._csv = open(self._ops['input'], mode='r',
                    encoding='utf-8', newline='')
            except OSError as e:
                err.Error.terminate(
                    'Cannot open input file\n\n',
                    err.Error.ErrorCodes.INPUT_FILE_OPENING_ERR)
        else:
            self._csv = sys.stdin
    
    def read(self):
        reader = csv.reader(self._csv, delimiter=self._ops['delimiter'])
        rownum = 1
        for row in reader:
            self._table[f'row{rownum}'] = dict()
            colnum = 1
            for col in row:
                self._table[f'row{rownum}'][f'col{colnum}'] = col
                colnum += 1
            rownum += 1
        print()
        print(self._table)
