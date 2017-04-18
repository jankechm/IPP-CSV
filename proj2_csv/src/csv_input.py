import sys

import src.err as err
import csv

class CSV(object):
    """CSV input"""
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
                    err.ErrorCodes.INPUT_FILE_OPENING_ERR)
        else:
            self._csv = sys.stdin
    
    def load_data(self):
        reader = csv.reader(self._csv, delimiter=self._ops['delimiter'])
        row_num = 1
        for row in reader:
            row_name = f'{self._ops["row_elem"]}{row_num}'
            self._table[f'{row_name}'] = dict()
            col_num = 1
            for col in row:
                col_name = f'{self._ops["col_elem"]}{col_num}'
                self._table[f'{row_name}'][f'{col_name}'] = col
                col_num += 1
            row_num += 1
        #print()
        #print(self._table)
        return self._table
