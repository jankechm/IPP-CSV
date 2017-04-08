import sys

import src.err as err

class XML(object):
    """XML"""
    def __init__(self, ops, file=None):
        self._file_address = file
        self._ops = ops

    def open(self):
        if (self._ops['output']):
            try:
                self._xml = open(self._ops['output'], mode='w',
                    encoding='utf-8', newline='')
            except OSError as e:
                err.Error.terminate(
                    'Cannot open output file\n\n',
                    err.Error.ErrorCodes.OUTPUT_FILE_OPENING_ERR)
        else:
            self._xml = sys.stdout
        #return self._xml